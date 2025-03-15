import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
load_dotenv()

def connect():
    # Establishes a connection to the database.
    try:
        connection = mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        port = int(os.getenv("DB_PORT")),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME"),
        )
        # print("Connection established!")  # For debugging purposes only
        return connection

    except Error as err:
        return (f"Something went wrong.[Error at server.py]: {err}")

def connect4seed():
    # Establishes a connection to the database.
    try:
        connection = mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        port = int(os.getenv("DB_PORT")),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        )
        # print("Connection established!")  # For debugging purposes only
        return connection

    except Error as err:
        return (f"Something went wrong.[Error at server.py]: {err}")