# app/models/weather_log_model.py

from app.utils.db_connection import get_db_connection

def create_weather_log_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS weather_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        city_id INT NOT NULL,
        temperature FLOAT,
        humidity FLOAT,
        wind_speed FLOAT,
        weather_condition VARCHAR(100),
        log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (city_id) REFERENCES cities(id)
    )
    """

    cursor.execute(query)
    conn.commit()
    print("weather_logs table created (or already exists).")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_weather_log_table()
