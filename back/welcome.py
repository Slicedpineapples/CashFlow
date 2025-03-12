import requests
from server import connect
import hashlib
from curr import get_currency

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
            # email = result[2]
            message = "Login successful!"
            # return f'userid{userid}, email{email}, country{counrty}, currency{currency}, message{message}'#debugging only
            return userid, email, counrty, currency, message

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

# print(login("pecs1", "pecs")) #Debugging only
# print(signUp("webdev", "webde@mail.com", "webdev", "1234567890")) #Debugging only