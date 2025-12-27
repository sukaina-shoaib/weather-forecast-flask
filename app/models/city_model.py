# app/models/city_model.py
from app.utils.db_connection import get_db_connection

def create_city_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS cities (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
         latitude FLOAT,
        longitude FLOAT
    )
    """

    cursor.execute(query)
    conn.commit()

    print("cities table created (or already exists).")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_city_table()
