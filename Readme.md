Land registry tracker

A program that takes in a dataset from HM land registry, and outputs both a report, and a database to be used potentially by other software.

## How to use
Upon starting the program, the software will ask for which dataset will be used. Depending on the optionn, different prompts will be given.
a - all data. looks for a file named pp-complete.csv.
y - use a dataset from a specific year. It asks for the last 2 digits of the year.
m - Look for a specific month. First, the month is specified, as a string. Then the year.

The program then manipulates the data, outputting an sql .db file, as well as a .txt file with a report.
Each are outputted into their own respective folder
## What it does
The program checks the file against the name given. If one is found, the program continues as normal, else the program terminates.
The program then takes the raw data and sanitise it, checking any non values and handles these. Several columns may be expected to be null values, and are not used by the program, so not read. Others may be edited and filled if they require a value. 

The data is then processed and placed into an SQL file, .db. 
THe program than handles the analytics. THis is done by opening a file, checking the name against any current ones, ensuring it does not overwrite any files. 
Each option is inputted into a file, obtaining the data with SQL functions. 
The program then terminates.


### Languages and frameworks
The program runs on python and its packages, as listed in main.py
SQL is also used, within sql_utils.py
