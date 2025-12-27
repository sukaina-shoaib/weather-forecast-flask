# app/utils/db_connection.py

import mysql.connector
from mysql.connector import Error

DB_NAME = "WeatherForecast"

def create_database_if_not_exists():
    """
    Checks if DB exists. If not, it creates it.
    """
    try:
        # Connect WITHOUT selecting any database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = conn.cursor()

        cursor.execute(f"SHOW DATABASES LIKE '{DB_NAME}'")
        result = cursor.fetchone()

        # if result:
        #     print(" Database already exists!")
        # else:
        #     cursor.execute(f"CREATE DATABASE {DB_NAME}")
        #     print("Database created successfully!")

        cursor.close()
        conn.close()

    except Error as e:
        print("Error while connecting to MySQL:", e)


def get_db_connection():
    """
    Connects to the WeatherForecast database AFTER ensuring it exists.
    """
    create_database_if_not_exists()

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=DB_NAME
        )
        return connection

    except Error as e:
        print(" Failed to connect to database:", e)
        return None



