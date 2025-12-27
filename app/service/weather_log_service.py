# app/services/weather_log_service.py
from app.utils.db_connection import get_db_connection

class WeatherLogService:

    @staticmethod
    def save_weather_log(city_id, temperature, humidity, wind_speed, condition):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO weather_logs 
            (city_id, temperature, humidity, wind_speed, weather_condition)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (city_id, temperature, humidity, wind_speed, condition))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_logs_by_city(city_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT * FROM weather_logs 
            WHERE city_id = %s ORDER BY log_time DESC
        """
        cursor.execute(query, (city_id,))
        logs = cursor.fetchall()
        cursor.close()
        conn.close()
        return logs

    @staticmethod
    def get_all_logs():
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM weather_logs ORDER BY log_time DESC LIMIT 500")
        rows = cur.fetchall()
        cur.close();
        conn.close()
        return rows

    def create_log(self, user_id, city_name, temperature, condition):
        """
        Convenience wrapper that matches the controller signature.
        """
        # 1. resolve/insert city
        from app.service.city_service import CityService
        city = CityService.get_city_by_name(city_name)
        if not city:
            city_id = CityService.add_city(city_name)
        else:
            city_id = city["id"]

        # 2. call the real method
        self.save_weather_log(city_id, temperature, None, None, condition)