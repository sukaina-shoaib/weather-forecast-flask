# app/models/favorite_model.py
from app.utils.db_connection import get_db_connection

def create_favorite_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS favorites (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        city_id INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (city_id) REFERENCES cities(id)
    )
    """

    cursor.execute(query)
    conn.commit()
    print("favorites table created (or already exists).")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_favorite_table()
