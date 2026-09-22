import pandas as pd
from data_utils import load_data, sanitise, report_missing, assess_nulls

def testFoo():
    print("Success")

#create a report
def analytics():
    print("analytics")

#load into sql

#used to handle and initialise the data
def openingSequence():
    print("yeet")

def main():
    print("hello world")
    #get file name
    fileName = "land-registry-july.csv"

    #read in the file name
    df_raw = load_data("raw/" + fileName)  #file to be read
    df_raw.head()

    #clean the data
    df = sanitise(df_raw)

    #find any missing values
    report_missing(df)  # check what's still null before you decide what to do with it
    
    print(assess_nulls(df))
    testFoo()
    #df.info()
    #df.describe(include="all")

    #load into sql (place into function)

    #the fun part (data analytics)


main()
#names of column headers
"""transaction_id, price, date_of_transfer, postcode, property_type,
old_new, duration, paon, saon, street, locality, town_city,
district, county, ppd_category_type, record_status"""