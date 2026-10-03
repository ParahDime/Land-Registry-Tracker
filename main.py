import pandas as pd
import sqlite3
from datetime import datetime
from pathlib import Path
from data_utils import load_data, sanitise, report_missing, assess_nulls
from sql_utils import sql_average_price_per_property_type, sql_get_dates, sql_average_property_price, sql_get_established, sql_get_freehold_property, sql_get_leasehold_property, sql_get_lower_percentile, sql_get_max_property_price, sql_get_newbuild, sql_get_special_trans, sql_get_standard_trans, sql_get_upper_percentile, sql_max_price_per_property_type, sql_min_price_per_property_type, sql_mode_price_per_property, sql_mode_property_price, sql_num_per_X, sql_total_market_sales, sql_total_sales

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

def generate_report():
    print("test")

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

def test_foo():
    print("Function called")

#create a report
def analytics(filePath, sql_db):
    print("Analytics report")

    #name file to debug
    path = Path(filePath + ".txt")
    stem, suffix = path.stem, path.suffix
    counter = 1

    print("Creating file...")
    while path.exists():
        path = path.with_name(f"{stem}_{counter}{suffix}")
        counter += 1

    now = datetime.now()
    report_datestamp = now.strftime("%Y-%m-%d")
    report_timestamp = now.strftime("%H:%M:%S")

    print("Processing...")
    with open(path, "w", encoding="utf-8") as f:
        f.write("Analytics Report" + "\n\n")
        f.write("Date: " + report_datestamp + "\n")
        f.write("Time:" + report_timestamp + "\n")
        with sqlite3.connect(DB_FILE) as engine:      
            f.write("Number of transations : " + str(sql_total_sales(engine)))
            start, end = sql_get_dates(engine)
            f.write("Start of dataset: ", start)
            f.write("End date of dataset: ", end)

        f.write("Dataset used: " + filePath + ".csv\n\n")
   
    print("File creation complete. Exiting...")
    return

#used to handle and initialise the data
def openingSequence():
    current_year = datetime.now().year
    
    while True:
        print("\n--- HM Land Registry Data Selection ---")
        print("  [m] Recent monthly release")
        print("  [y] Specific Year")
        print("  [a] All Data (Complete dataset)")

        current_full_year = datetime.now().year
        current_short_year = current_full_year % 100

        choice = input("Select option (m/y/a): ").strip().lower()
            
        if choice == 'a':
            return "pp-complete"
            
        # Specific Year: Gets last 2 digits of the year
        elif choice == 'y':
            year_input = input("Enter year (last 2 digits, e.g., 23): ").strip()
            if year_input.isdigit() and len(year_input) <= 2:
                return f"pp-{year_input.zfill(2)}"
            print("Invalid year. Please enter a 2-digit number.")
            
        # Recent Monthly Release: Asks for month name ('july') and year (last 2 digits)
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
#names of column headers

#null columns street or postcode - can be fields, orchards etc