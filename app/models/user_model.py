# app/models/user_model.py
from app.utils.db_connection import get_db_connection

def create_user_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    cursor.execute(query)
    conn.commit()

    print("users table created (or already exists).")

    cursor.close()
    conn.close()


# ONLY RUN WHEN FILE IS EXECUTED DIRECTLY
if __name__ == "__main__":
    create_user_table()
