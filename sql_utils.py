import pandas as pd
import sqlite3

def sql_total_sales(engine):
    cursor = engine.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    return int(count)

 #get metrics
def sql_num_per_X(engine) -> list[tuple]:
    #transaction numbers per X
    #f d s t o
    query = """
        SELECT 
            CASE property_type
                WHEN 'F' THEN 'Flat'
                WHEN 'T' THEN 'Terraced'
                WHEN 'S' THEN 'Semi-Detached'
                WHEN 'D' THEN 'Detached'
                ELSE 'Other'
            END AS property_name,
            COUNT(*) AS transaction_count
        FROM transactions
        GROUP BY property_type
        ORDER BY transaction_count DESC;
    """
    cursor = engine.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def sql_get_dates(engine) -> tuple[str, str]:
    query = """
        SELECT 
            MIN(date_of_transfer) AS start_date, 
            MAX(date_of_transfer) AS end_date 
        FROM transactions
    """
    cursor = engine.cursor()
    cursor.execute(query)
    start_date, end_date = cursor.fetchone()
    
    #Conversion to string
    start_str = str(start_date) if start_date else "Unknown"
    end_str = str(end_date) if end_date else "Unknown"

    return start_str, end_str

def sql_total_market_sales():
    #total market value of sales
    print("hello world")

def sql_average_property_price():
    #value per properties averages
    print("hello world")

def sql_average_price_per_property_type():
    #average prices
    print("hello world")

def sql_mode_property_price():
    #mode value
    print("hello world")

def sql_mode_price_per_property():
    print("hello world")

def sql_min_price_per_property_type():
    #min values (plus data
    print("hello world")

#max value
def sql_get_max_property_price():
    print("hello world")

#max value per property price
def sql_max_price_per_property_type():
    print("hello world")

#IQR and percentiles
def sql_get_upper_percentile():
    print("hello world")

def sql_get_lower_percentile():
    print("hello world")

#freehold vs leasehold
   
 #trans per property type (+ stats)
def sql_get_leasehold_property():
    print("hello world")

def sql_get_freehold_property():

    print("hello world")

#new build vs established
def sql_get_newbuild():
    print("hello world")

def sql_get_established():
    print("hello world")

#cat a vs cat b sales
def sql_get_standard_trans(): #standard property purchase
    print("hello world")

def sql_get_special_trans(): #covers repos, buy to let etc
    print("hello world")