import pandas as pd
from data_utils import load_data, sanitise, report_missing, assess_nulls
import sqlite3
import datetime
from pathlib import Path

DB_FILE = "land_registry.db"

def main():
    fileName = openingSequence()
    #get file name
    print(fileName)
    #read in the file name
    df_raw = load_data("raw/" + fileName)  #file to be read
    df_raw.head()

    header_list = ["transaction_id", "price", "date_of_transfer", "postcode", "property_type",
    "old_new", "duration", "paon", "saon", "street", "locality", "town_city",
    "district", "county", "ppd_category_type", "record_status"]
    #add the data to the current file being worked on
    df_raw.columns = header_list

    #clean the data
    df = sanitise(df_raw)
    #find any missing values
    report_missing(df)  # check what's still null before you decide what to do with it
    #expose any null values
    print(assess_nulls(df))
    #obtain basic information on the dataset
    df.info()
    df.describe(include="all")
    #move the data into an SQL file
    push_to_SQL(df)


    analytics(fileName, df)

def generate_report():
    print("test")

#take dataset and place it into an sql file
def push_to_SQL(df: pd.DataFrame) -> None:
    #open/create sql file, name of file
    engine = sqlite3.connect("land_registry.db")
    df.to_sql("transactions", engine, if_exists="replace", index=False)
    engine.close()
    print("Data successfully loaded into SQL.")
    #convert into an sql file

    #close the sql file

    #try catch when using
    print("Hello")
    return

def test_foo():
    print("Success")

#create a report
def analytics(fileName, df):
    print("Analytics")

    path = Path(fileName)
    stem, suffix = path.stem, path.suffix
    counter = 1

    while path.exists():
        path = path.with_name(f"{stem}_{counter}{suffix}")
        counter += 1

    with open(path, "w", encoding="utf-8") as f:
        f.write("hello world" + "\n")
    #get metrics
    #transaction numbers per X
    #dates used within hte analytics
    #total market value of sales

    #value per properties averages
    #average prices
    #mode value

    #min values (plus data
    #max value
    #IQR and percentiles
    #no outside standard dist
    #trans per property type (+ stats)
    #freehold vs leasehold
    #new build vs established
    #get a year
    #cat a vs cat b sales


#used to handle and initialise the data
def openingSequence():
    current_year = datetime.datetime.now().year
    
    while True:
        print("\n--- HM Land Registry Data Selection ---")
        print("  [m] Recent monthly release")
        print("  [y] Specific Year")
        print("  [a] All Data (Complete dataset)")

        current_full_year = datetime.datetime.now().year
        current_short_year = current_full_year % 100

        choice = input("Select option (m/y/a): ").strip().lower()
            
        if choice == 'a':
            return "pp-complete.csv"
            
        # Specific Year: Gets last 2 digits of the year
        elif choice == 'y':
            year_input = input("Enter year (last 2 digits, e.g., 23): ").strip()
            if year_input.isdigit() and len(year_input) <= 2:
                return f"pp-{year_input.zfill(2)}.csv"
            print("Invalid year. Please enter a 2-digit number.")
            
        # Recent Monthly Release: Asks for month name ('july') and year (last 2 digits)
        elif choice == 'm':
            month_input = input("Enter month (e.g., july): ").strip().capitalize()
            year_input = input("Enter year (last 2 digits, e.g., 23): ").strip()
            
            if len(month_input) >= 3:
                month_abbr = month_input[:3]
                year_val = year_input if (year_input.isdigit() and len(year_input) <= 2) else "26"
                return f"pp-{month_abbr}{year_val}.csv"
            print("Invalid input.")
            
        else:
            print("Invalid choice. Please enter 'm', 'y', or 'a'.")


main()
#names of column headers

#null columns street or postcode - can be fields, orchards etc