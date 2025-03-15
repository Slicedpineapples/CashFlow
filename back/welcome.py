import requests
from server import connect
import hashlib
from curr import get_currency
from flask import request, jsonify
from server import connect
from utils import userSecurityToken


global message
message = ""

def signUp(username, email, password, phone):
    username = username
    email = email
    password = password # password hashed at the front end
    phone = phone
    ustoken = 0
    sessionstatus = 0

    try:
        connection = connect()
        cursor = connection.cursor()

        # Check if user already exists
        sql_check = "SELECT id FROM user WHERE username = %s OR email = %s OR phone = %s"
        values_check = (username, email, phone)
        cursor.execute(sql_check, values_check)
        result_check = cursor.fetchone()
        
        # Fetch all remaining results to avoid "Unread result found" error
        cursor.fetchall()

        if result_check:
            message = "The username, email or phone has already been used. \nTry using different credentials."
            return None, message

        # Get User IP and Region
        ip_response = requests.get('https://api.ipify.org?format=json')
        ip_data = ip_response.json()
        user_ip = ip_data['ip']
        geolocation_response = requests.get(f'https://ipapi.co/{user_ip}/country_name')
        region = geolocation_response.text
        currency = get_currency(region)
        ustoken = userSecurityToken()

        # Insert new user (using a new cursor)
        sql = "INSERT INTO user (email, phone, region, currency, userName, password, ustoken, session) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (email, phone, region, currency, username, password, ustoken, sessionstatus)
        
        cursor2 = connection.cursor()
        cursor2.execute(sql, values)
        connection.commit()
        message = "User created successfully!"
        userId = cursor2.lastrowid
        cursor2.close()

    except Exception as e:
        message = f"Something went wrong: {e}"
        print("Error:", e)
        userId = None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return userId, message

def login(username, password):
    # print("Login to your account")
    # if username == None and password == None:
    #     username = input("Enter your username: ")
    #     password = input("Enter your password: ")
    # else:
    # password = hashlib.sha256(password.encode()).hexdigest()
    username = username
    password = password # password hashed at the front end
    ust = 0 # default ustoken
    sessionstatus = 0 # Default session status

    try:
        connection = connect()
        cursor = connection.cursor()
        
        sql = "SELECT * FROM user WHERE userName = %s AND password = %s"
        values = (username, password)
        cursor.execute(sql, values)
        result = cursor.fetchone()

        if result:
            ust = userSecurityToken() # Generate a new ustoken for the current login session
            print(ust)
            # Update session status to 1
            update_sql = "UPDATE user SET ustoken = %s, session = TRUE WHERE userName = %s"
            update_values = (ust, username)
            cursor.execute(update_sql, update_values)
            connection.commit()
            print(f"Rows affected: {cursor.rowcount}")  # Debugging: Check if update actually happens

            message = "Login successful!"
            # return userid, email, counrty, currency, phone, message
            return ust, message

        else:
            message = "Invalid username or password"
            ust = None
            update_sql = "UPDATE user SET session = FALSE WHERE userName = %s"
            update_values = (username,)
            cursor.execute(update_sql, update_values)
            connection.commit()
            return ust, message

    except Exception as e:
        print("Error:", e)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def fetchuserdata(ustoken):
    try:
        connection = connect()
        cursor = connection.cursor()

        sql = "SELECT * FROM user WHERE ustoken = %s"
        values = (ustoken,)
        cursor.execute(sql, values)
        result = cursor.fetchone()

        if result:
            userid = result[0]
            email = result[1]
            counrty = result[3]
            currency = result[4]
            phone = result[2]
            message = "User data fetched successfully!"
            return userid, email, counrty, currency, phone, message

        else:
            message = "Invalid user security token"
            return None, message

    except Exception as e:
        print("Error:", e)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

        
# print(fetchuserdata("4c5e4d18bdc60e4450a82740376e961f853c58956f4ebe2114f0675b69372914"))