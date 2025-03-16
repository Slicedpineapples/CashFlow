import datetime
import os
import requests
from server import connect, connect4seed
from mysql.connector import Error
import string
import random
import hashlib

def makeDir():
    folder = 'reports'
    if not os.path.exists(folder):
        os.makedirs(folder)
    folder = 'reports/AssetsReports'
    if not os.path.exists(folder):
        os.makedirs(folder)

    folder = 'reports/LiabilitiesReports'
    if not os.path.exists(folder):
        os.makedirs(folder)

    folder = 'reports/ExpensesReports'
    if not os.path.exists(folder):
        os.makedirs(folder)

    folder = 'reports/IncomeReports'
    if not os.path.exists(folder):
        os.makedirs(folder)
    folder = 'reports/monthlyReports'
    if not os.path.exists(folder):
        os.makedirs(folder)
    folder = 'logs'
    if not os.path.exists(folder):
        os.makedirs(folder)

def Date():
    defaultdate = datetime.datetime.now()
    # global month #Debugging only
    year = input("Year: ")
    month = input("Month: ")
    day = input("Day: ")

    if (year == "" and month == "" and day == ""):
        date = datetime.datetime(defaultdate.year, defaultdate.month, defaultdate.day)
        month = defaultdate.month
    elif (year == "" and month == "" and day != ""):
        date = datetime.datetime(defaultdate.year, defaultdate.month, int(day))
        month = defaultdate.month
    elif (year == "" and month != "" and day == ""):
        date = datetime.datetime(defaultdate.year, int(month), defaultdate.day)
    elif (year == "" and month != "" and day != ""):
        date = datetime.datetime(defaultdate.year, int(month), int(day))
    elif (year != "" and month == "" and day == ""):
        date = datetime.datetime(int(year), defaultdate.month, defaultdate.day)
        month = defaultdate.month
    elif (year != "" and month == "" and day != ""):
        date = datetime.datetime(int(year), defaultdate.month, int(day))
        month = defaultdate.month
    elif (year != "" and month != "" and day == ""):
        date = datetime.datetime(int(year), int(month), defaultdate.day)
    else:
        date = datetime.datetime(int(year), int(month), int(day))
    # print(date, month) # Debugging purpose only

    # # Combining bith functins for ease when calling them in my other procedures

    # month = int(month)
    # # print(f'Month is {month}, from Convert function') #Debugging only
    # month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    # # print(month_names[month - 1])  #Debugging only
    # monthName = month_names[month - 1]
    return date

def Convert(month):
    month = int(month)
    month_names = ['January', 'February', 'March', 'April', 'May', 'Jun', 'July', 'August', 'September', 'October', 'November', 'December']
    # print(month_names[month - 1])  #Debugging only
    monthName = month_names[month - 1]
    return monthName

def getExchangeRate(target_currency, base_currency="HUF"):

    url = f"https://open.er-api.com/v6/latest/{base_currency}" # Using the free API
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception("Failed to fetch exchange rates from the API.")
    
    data = response.json()
    
    if data.get("result") != "success":
        raise Exception("Failed to retrieve valid data from the API.")
    
    rates = data["rates"]
    
    if target_currency not in rates:
        raise Exception(f"Exchange rate for {target_currency} not found.")
    
    return rates[target_currency]

def seed():
    # Check if the database exists. If not, seed it with a schema.
    try:
        connection = connect4seed() # using the first function to connect to the database
        cursor = connection.cursor()
        # Check if the database exists
        database_name = os.getenv("DB_NAME")
        cursor.execute(f"SHOW DATABASES LIKE '{database_name}'")
        result = cursor.fetchone()

        if result:
            print(f"Database '{database_name}' already exists.")
        else:
            print(f"Database '{database_name}' does not exist. Trying to create and seed the database...")
            # Create the database
            cursor.execute(f"CREATE DATABASE {database_name}")
            connection.database = database_name  # Switch to the new database

            # Seed the database with the schema
            schema_path = "cashflow.sql"  # Update this path if necessary
            with open(schema_path, "r") as schema_file:
                schema_sql = schema_file.read()
                for statement in schema_sql.split(";"):  # Split on ';' for individual statements
                    if statement.strip():  # Skip empty statements
                        cursor.execute(statement)

            print(f"Database '{database_name}' has been created and seeded successfully.")

        cursor.close()
        connection.close()

    except Error as err:
        print(f"Something went wrong: {err}")

# seed() # Debugging only

def userSecurityToken():
    characters = string.ascii_letters + string.digits + string.punctuation
    random_combination = ''.join(random.choices(characters, k=10))
    hashUST = hashlib.sha256(random_combination.encode()).hexdigest()
    return hashUST

# print(userSecurityToken()) # Debugging only
def ustVerify(ustoken):
    connection = connect()
    cursor = connection.cursor()

    sql = "SELECT ustoken, session FROM user WHERE ustoken = %s"
    values = (ustoken,)
    cursor.execute(sql, values)
    result = cursor.fetchone()
    session = result[1] if result else None
    cursor.close()
    connection.close()
    if result and session == 1:
        return True
    else:
        return False
    
# print(ustVerify("3dd7aefdf0d4a1cd4a89b5089a9c1c0ca269d3dd020694c0148fcb118f111255")) # Debugging only
def userFetch(ust):
    if ustVerify(ust) == False:
        return "Invalid User Seed Token"
    else:
        connection = connect()
        cursor = connection.cursor()
        sql = "SELECT * FROM user WHERE ustoken = %s"
        values = (ust,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        result = {
            "userId": result[0],
            "email": result[1],
            "phone": result[2],
            "country": result[3],
            "currency": result[4],
            "username": result[5]
        }
        return result

# print(userFetch("bdd8a07c295e11292575d89194c2016853259edc00021d164b56a96c5316d2a7")) # Debugging only