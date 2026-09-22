import pandas as pd
from data_utils import load_data, sanitise, report_missing, assess_nulls
#sanitise the data

#clean the data


def main():
    print("hello world")
    #get file name
    fileName = "lan-registry-july.csv"

    #read in the file name
    df_raw = load_data(fileName)  #file to be read
    df_raw.head()

    #clean the data
    df = sanitise(df_raw)

    #find any missing values
    report_missing(df)  # check what's still null before you decide what to do with it

    assess_nulls(df)
    
    df.info()
    df.describe(include="all")