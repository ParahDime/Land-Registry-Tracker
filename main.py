import pandas as pd
from data_utils import load_data, sanitise, report_missing, assess_nulls
import sqlite3

def main():
    print("hello world")
    #get file name
    fileName = "land-registry-july.csv"

    #read in the file name
    df_raw = load_data("raw/" + fileName)  #file to be read
    df_raw.head()

    header_list = ["transaction_id", "price", "date_of_transfer", "postcode", "property_type",
    "old_new", "duration", "paon", "saon", "street", "locality", "town_city",
    "district", "county", "ppd_category_type", "record_status"]
    df_raw.columns = header_list

    #clean the data
    df = sanitise(df_raw)

    #find any missing values
    report_missing(df)  # check what's still null before you decide what to do with it
    
    print(assess_nulls(df))
    test_foo()
    df.info()
    df.describe(include="all")

    push_to_SQL(df)
    #load into sql (place into function)

    #the fun part (data analytics)

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

def test_foo():
    print("Success")

#create a report
def analytics():
    print("analytics")

#used to handle and initialise the data
def openingSequence():
    print("yeet")


main()
#names of column headers

#null columns street or postcode - can be fields, orchards etc