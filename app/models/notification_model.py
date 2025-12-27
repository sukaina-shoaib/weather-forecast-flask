# app/models/notification_model.py
from app.utils.db_connection import get_db_connection

def create_notification_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS notifications (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        message TEXT NOT NULL,
        is_read BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """

    cursor.execute(query)
    conn.commit()
    print("notifications table created (or already exists).")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_notification_table()
