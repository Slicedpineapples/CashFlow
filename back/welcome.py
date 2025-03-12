import requests
from server import connect
import hashlib
from curr import get_currency
from flask import request, jsonify
from server import connect


global message
message = ""

def signUp(username, email, password, phone):
    userame = username
    email = email
    password = hashlib.sha256(password.encode()).hexdigest()
    phone = phone

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

        # Insert new user (using a new cursor)
        sql = "INSERT INTO user (email, phone, region, currency, userName, password) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (email, phone, region, currency, userName, password)
        
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
    username = username
    password = hashlib.sha256(password.encode()).hexdigest()

    try:
        connection = connect()
        cursor = connection.cursor()
        
        sql = "SELECT * FROM user WHERE userName = %s AND password = %s"
        values = (username, password)
        cursor.execute(sql, values)
        result = cursor.fetchone()

        if result:
            userid = result[0]
            email = result[1]
            counrty = result[3]
            currency = result[4]
            phone = result[2]
            message = "Login successful!"
            # return f'userid{userid}, email{email}, country{counrty}, currency{currency}, message{message}'#debugging only
            return userid, email, counrty, currency, phone, message

        else:
            message = "Invalid username or password"
            return None, message

    except Exception as e:
        print("Error:", e)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

import hashlib
from server import connect
from curr import get_currency  # Assuming this function exists to get currency based on country

# def updateProfile(userId):
#     try:
#         connection = connect()
#         cursor = connection.cursor()

#         # User input for new values (can be adjusted for a form or API later)
#         new_email = input("Enter new email: ")
#         new_phone = input("Enter new phone number: ")
#         new_country = input("Enter new country: ")
#         new_currency = get_currency(new_country)

#         # Get the old user values from the database
#         cursor.execute("SELECT email, phone, region, currency FROM user WHERE id = %s", (userId,))
#         old_values = cursor.fetchone()

#         # If no user is found with this userId
#         if not old_values:
#             return "User not found."

#         # Check if the new value is provided, else keep the old value
#         if not new_email:
#             new_email = old_values[0]  # Keep old email
#         if not new_phone:
#             new_phone = old_values[1]  # Keep old phone number
#         if not new_country:
#             new_country = old_values[2]  # Keep old country
#         if not new_currency:
#             new_currency = old_values[3]  # Keep old currency

#         # Update the user profile with the new values
#         sql = """
#             UPDATE user
#             SET email = %s, phone = %s, region = %s, currency = %s
#             WHERE id = %s
#         """
#         values = (new_email, new_phone, new_country, new_currency, userId)
#         cursor.execute(sql, values)
#         connection.commit()

#         message = "Profile updated successfully!"

#     except Exception as e:
#         message = f"Something went wrong: {e}"
#         print("Error:", e)

#     finally:
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close()

#     return message




        
