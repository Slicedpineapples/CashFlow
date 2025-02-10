import requests
from server import connect
import hashlib

global message
message = ""

def signUp(username, email, password, phone):
    # print("Sign up for a new account")
    # userName = input("Enter a username: ")
    # email = input("Enter your email: ")
    # password = input("Enter a password: ")
    # phone = input("Enter your phone number: ")
    userName = username
    email = email
    password = hashlib.sha256(password.encode()).hexdigest()
    phone = phone

    try:
        ip_response = requests.get('https://api.ipify.org?format=json')
        ip_data = ip_response.json()
        user_ip = ip_data['ip']
        geolocation_response = requests.get(f'https://ipapi.co/{user_ip}/region')
        region = geolocation_response.text

        signup = connect()  # Assuming connect returns a database connection
        cursor = signup.cursor()

        sql = "INSERT INTO user (email, phone, region, userName, password) VALUES (%s, %s, %s, %s, %s)"
        values = (email, phone, region, userName, password)
        cursor.execute(sql, values)
        signup.commit()
        message = "User created successfully!"
        

    except Exception as e:
        message = "Something went wrong:", e
        print("Error:", e)

    finally:
        if cursor:
            cursor.close()
        if signup:
            signup.close()
    userId = cursor.lastrowid
    # print("Your user ID is:", userId) #Debugging only
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
        
        sql = "SELECT id, userName, email FROM user WHERE userName = %s AND password = %s"
        values = (username, password)
        cursor.execute(sql, values)
        result = cursor.fetchone()

        if result:
            userid = result[0]
            email = result[2]
            message = "Login successful!"
            return userid, email, message

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

# print(login("helix", "helix")) #Debugging only
# print(signUp("webdev", "webde@mail.com", "webdev", "1234567890")) #Debugging only