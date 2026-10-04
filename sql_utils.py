import pandas as pd
import sqlite3
import statistics
from collections import defaultdict

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

def sql_total_market_sales(engine):
    #total market value of sales
    query = "SELECT SUM(price) FROM transactions"
    
    cursor = engine.cursor()
    cursor.execute(query)
    total_sales = cursor.fetchone()[0]
    
    #return 0 if error / not available
    return total_sales if total_sales is not None else 0.0

def sql_total_sales_county(engine) -> list[tuple]:
    """Queries total sales and transaction count grouped by county."""
    query = """
        SELECT 
            county,
            COUNT(*) AS transaction_count,
            SUM(price) AS total_sales
        FROM transactions
        WHERE county IS NOT NULL AND county != ''
        GROUP BY county
        ORDER BY total_sales DESC;
    """
    cursor = engine.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def sql_average_property_price(engine) -> list[tuple]:
    #value per properties averages per county
    query = """
        SELECT 
            county,
            AVG(price) AS average_price
        FROM transactions
        WHERE county IS NOT NULL AND county != ''
        GROUP BY county
        ORDER BY average_price DESC;
    """
    cursor = engine.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def sql_average_price_per_property_type(engine) -> list[tuple]:
    #average prices
    query = """
        SELECT 
            county,
            CASE property_type
                WHEN 'F' THEN 'Flat'
                WHEN 'T' THEN 'Terraced'
                WHEN 'S' THEN 'Semi-Detached'
                WHEN 'D' THEN 'Detached'
                ELSE 'Other'
            END AS property_name,
            AVG(price) AS average_price
        FROM transactions
        WHERE county IS NOT NULL AND county != ''
        GROUP BY county, property_type
        ORDER BY county, average_price DESC;
    """
    cursor = engine.cursor()
    cursor.execute(query)
    return cursor.fetchall()



""" HERE - TO TEST """
def sql_min_price_per_property_type(engine) -> list[tuple]:
    #min values (plus data
    query = """
        SELECT 
            county,
            CASE property_type
                WHEN 'F' THEN 'Flat'
                WHEN 'T' THEN 'Terraced'
                WHEN 'S' THEN 'Semi-Detached'
                WHEN 'D' THEN 'Detached'
                ELSE 'Other'
            END AS property_name,
            MIN(price) AS min_price
        FROM transactions
        WHERE county IS NOT NULL AND county != ''
        GROUP BY county, property_type
        ORDER BY county, min_price ASC;
    """
    cursor = engine.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#max value per property price
def sql_max_price_per_property_type(engine) -> list[tuple]:
        query = """
        SELECT 
            county,
            CASE property_type
                WHEN 'F' THEN 'Flat'
                WHEN 'T' THEN 'Terraced'
                WHEN 'S' THEN 'Semi-Detached'
                WHEN 'D' THEN 'Detached'
                ELSE 'Other'
            END AS property_name,
            MAX(price) AS min_price
        FROM transactions
        WHERE county IS NOT NULL AND county != ''
        GROUP BY county, property_type
        ORDER BY county, min_price ASC;
        """
        cursor = engine.cursor()
        cursor.execute(query)
        return cursor.fetchall()

#IQR and percentiles
def sql_get_upper_percentile(engine) -> list[tuple]:
    query = """
        SELECT county, property_type, price 
        FROM transactions 
        WHERE county IS NOT NULL AND county != '' AND price IS NOT NULL;
    """
    cursor = engine.cursor()
    cursor.execute(query)
    
    # Group prices by (county, property_type)
    grouped_prices = defaultdict(list)
    for county, prop_type, price in cursor.fetchall():
        readable_type = {
            'F': 'Flat',
            'T': 'Terraced',
            'S': 'Semi-Detached',
            'D': 'Detached'
        }.get(prop_type, 'Other')
        
        grouped_prices[(county, readable_type)].append(price)
        
    # Compute upper quartile for each group
    results = []
    for (county, prop_type), prices in grouped_prices.items():
        if prices:
            prices.sort()
            # n=4 splits data into quartiles; index 2 is the 75th percentile (upper quartile)
            upper_q = statistics.quantiles(prices, n=4)[2] if len(prices) >= 4 else max(prices)
            results.append((county, prop_type, upper_q))
            
    # Sort results alphabetically by county
    results.sort(key=lambda x: x[0])
    return results

def sql_get_lower_percentile(engine) -> list[tuple]:
    query = """
        SELECT county, property_type, price 
        FROM transactions 
        WHERE county IS NOT NULL AND county != '' AND price IS NOT NULL;
    """
    cursor = engine.cursor()
    cursor.execute(query)
    
    # Group prices by (county, property_type)
    grouped_prices = defaultdict(list)
    for county, prop_type, price in cursor.fetchall():
        readable_type = {
            'F': 'Flat',
            'T': 'Terraced',
            'S': 'Semi-Detached',
            'D': 'Detached'
        }.get(prop_type, 'Other')
        
        grouped_prices[(county, readable_type)].append(price)
        
    # Compute lower quartile for each group
    results = []
    for (county, prop_type), prices in grouped_prices.items():
        if prices:
            prices.sort()
            # n=4 splits data into quartiles; index 0 is the 25th percentile (lower quartile)
            lower_q = statistics.quantiles(prices, n=4)[0] if len(prices) >= 4 else min(prices)
            results.append((county, prop_type, lower_q))
            
    # Sort results alphabetically by county
    results.sort(key=lambda x: x[0])
    return results

#freehold vs leasehold
   
 #trans per property type (+ stats)
def sql_get_leasehold_property(engine) -> list[tuple]:
    query = """
        SELECT 
            county,
            COUNT(*) AS leasehold_count
        FROM transactions
        WHERE duration = 'L' AND county IS NOT NULL AND county != ''
        GROUP BY county
        ORDER BY leasehold_count DESC;
    """
    cursor = engine.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#freehold by county
def sql_get_freehold_property(engine) -> list[tuple]:
    query = """
        SELECT 
            county,
            COUNT(*) AS freehold_count
        FROM transactions
        WHERE duration = 'F' AND county IS NOT NULL AND county != ''
        GROUP BY county
        ORDER BY freehold_count DESC;
    """
#new build vs established
def sql_get_newbuild(engine) -> int:
    query = """
        SELECT COUNT(*) 
        FROM transactions 
        WHERE old_new = 'Y';
    """
    cursor = engine.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result else 0

def sql_get_established(engine) -> int:
        query = """
            SELECT COUNT(*) 
            FROM transactions 
            WHERE old_new = 'N';
        """
        cursor = engine.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else 0

#cat a vs cat b sales
def sql_get_standard_trans(engine) -> int: #standard property purchase
    query = """
        SELECT COUNT(*) 
        FROM transactions 
        WHERE ppd_category_type = 'A';
    """
    cursor = engine.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result else 0

def sql_get_special_trans(engine) -> int: #covers repos, buy to let etc
    query = """
        SELECT COUNT(*) 
        FROM transactions 
        WHERE ppd_category_type = 'B';
    """
    cursor = engine.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result else 0