import pandas as pd
import sqlite3
from datetime import datetime
from pathlib import Path
from data_utils import load_data, sanitise, report_missing, assess_nulls
from sql_utils import sql_average_price_per_property_type, sql_get_dates, sql_total_sales_county, sql_average_property_price, sql_get_established, sql_get_freehold_property, sql_get_leasehold_property, sql_get_lower_percentile, sql_max_price_per_property_type, sql_get_newbuild, sql_get_special_trans, sql_get_standard_trans, sql_get_upper_percentile, sql_max_price_per_property_type, sql_min_price_per_property_type, sql_num_per_X, sql_total_market_sales, sql_total_sales
from collections import defaultdict

#name definitions for paths
DB_FOLDER = Path("databases")
DB_FOLDER.mkdir(parents=True, exist_ok=True)

DB_FILE = DB_FOLDER / "land_registry.db"

def main():
    filePath = openingSequence()
    fileName = filePath + ".csv"
    print("filename selected: " + fileName)

    #read in the file name
    df_raw = load_data("raw/" + fileName)  #file to be read
    df_raw.head()

    #headers defined and added to the dataset
    header_list = ["transaction_id", "price", "date_of_transfer", "postcode", "property_type",
    "old_new", "duration", "paon", "saon", "street", "locality", "town_city",
    "district", "county", "ppd_category_type", "record_status"]
    df_raw.columns = header_list

    #data sanitising
    df = sanitise(df_raw)
    #find any missing values
    report_missing(df)
    print(assess_nulls(df))

    #obtain basic information on the dataset
    df.info()
    df.describe(include="all")

    #move the data into an SQL file
    sql_db = push_to_SQL(df)


    analytics(filePath, sql_db)
    return

#take dataset and place it into an sql file
def push_to_SQL(df: pd.DataFrame) -> None:
    #open/create sql file, name of file
    try:
        with sqlite3.connect(DB_FILE) as engine:
            df.to_sql("transactions", engine, if_exists="replace", index=False)
        print("Data successfully loaded into SQL.")
    except sqlite3.Error as e:
        print(f"Database error occurred: {e}")
    except PermissionError:
        print(f"Permission denied: Could not write to '{DB_FILE}'. Is the database open in another program?")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return str(DB_FILE)

#create a report
def analytics(filePath, sql_db):
    #enter where the reports go
    REPORT_FOLDER = Path("reports")
    REPORT_FOLDER.mkdir(parents=True, exist_ok=True)
    print("Analytics report")

    #name file to debug
    stem = filePath 
    suffix = ".txt"
    path = REPORT_FOLDER / f"{stem}{suffix}"
    counter = 1

    print("Creating file...")
    while path.exists():
        path = path.with_name(f"{stem}_{counter}{suffix}")
        counter += 1

    money = lambda v: f"£{v:,.0f}"
    now = datetime.now() 

    print("Processing...")
    with open(path, "w", encoding="utf-8") as f:
        f.write("Analytics Report" + "\n\n")
        #BASICS
        f.write("Dataset used: " + filePath + ".csv\n\n")
        f.write(f"Date: {now:%Y-%m-%d} \n")
        f.write(f"Time: {now:%H:%M:%S}\n")

        with sqlite3.connect(DB_FILE) as engine:      
            f.write("Number of transations: " + str(sql_total_sales(engine)))
            start, end = sql_get_dates(engine)
            f.write("Start of dataset: {str(start)}\n")
            f.write("End date of dataset: {str(end)} \n\n")

            f.write("Total price of houses sold: £" + str(sql_total_market_sales(engine)))           

            f.write("Property transactions by type: \n")
            property_breakdown = sql_num_per_X(engine)
            for property_name, count in property_breakdown:
                f.write(f"{property_name}: {count} transactions \n\n")

            #COUNTRY STATS
            #get newbuild
            f.write("Total number of new build house sales: " + str(sql_get_newbuild(engine)))
            #get established
            f.write("Total number of established sales: " + str(sql_get_established(engine)))
            #standard sales
            f.write("Number of category A sales (Regular house purchases): " + str(sql_get_standard_trans(engine)))
            #repos and other
            f.write("Number of category B sales (land sales, reposessions, etc): " + str(sql_get_special_trans(engine)))

            #COUNTY WIDE
            #lookup
            totals = {c: (n, t) for c, n, t in sql_total_sales_county(engine)}
            avg = dict(sql_average_property_price(engine))
            lease = dict(sql_get_leasehold_property(engine))
            free = dict(sql_get_freehold_property(engine))

            #Get statistics per county
            stats = defaultdict(lambda: defaultdict(dict))
            metric_queries = {
                "avg": sql_average_price_per_property_type,
                "min": sql_min_price_per_property_type,
                "max": sql_max_price_per_property_type,
                "lower": sql_get_lower_percentile,
                "upper": sql_get_upper_percentile,
            }
            for metric, query_fn in metric_queries.items():
                for county, ptype, value in query_fn(engine):
                    stats[county][ptype][metric] = value

            f.write("\n=== COUNTIES ===\n")
            #output in county alphabetical
            for county in sorted(totals):
                count, total = totals[county]
                f.write(f"\n{county}\n")
                f.write(f"  Sales: {count:,} | Total: {money(total)} | Average: {money(avg.get(county, 0))}\n")
                f.write(f"  Leasehold: {lease.get(county, 0):,} | Freehold: {free.get(county, 0):,}\n")
                f.write("  By property type:\n")
                for ptype, m in sorted(stats[county].items()):
                    #Guard conditions used
                    f.write(
                        f"    - {ptype}: avg {money(m.get('avg', 0))} | "
                        f"min {money(m.get('min', 0))} | max {money(m.get('max', 0))} | "
                        f"LQ {money(m.get('lower', 0))} | UQ {money(m.get('upper', 0))}\n"
                    )
   
    print("File creation complete. Exiting...")
    return

#used to handle and initialise the data
def openingSequence():
    while True:
        print("\n--- HM Land Registry Data Selection ---")
        print("  [m] Recent monthly release")
        print("  [y] Specific Year")
        print("  [a] All Data (Complete dataset)")

        choice = input("Select option (m/y/a): ").strip().lower()

        #look for a specific file
        if choice == 'a':
            return "pp-complete"
            
        #Get a specific year
        elif choice == 'y':
            year_input = input("Enter year (last 2 digits, e.g., 23): ").strip()
            if year_input.isdigit() and len(year_input) <= 2:
                return f"pp-{year_input.zfill(2)}"
            print("Invalid year. Please enter a 2-digit number.")
            
        #Get month and the year
        elif choice == 'm':
            month_input = input("Enter month (e.g., july): ").strip().capitalize()
            year_input = input("Enter year (last 2 digits, e.g., 23): ").strip()
            
            if len(month_input) >= 3:
                month_abbr = month_input[:3]
                year_val = year_input if (year_input.isdigit() and len(year_input) <= 2) else "26"
                return f"pp-{month_abbr}{year_val}"
            print("Invalid input.")
            
        else:
            print("Invalid choice. Please enter 'm', 'y', or 'a'.")


main()