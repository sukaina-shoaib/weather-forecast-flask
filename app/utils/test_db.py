from app.utils.db_connection import create_database_if_not_exists, get_db_connection

create_database_if_not_exists()

conn = get_db_connection()
if conn:
    print("Database connection OK!")
else:
    print("Connection failed.")
