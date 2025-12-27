# app/services/city_service.py

from app.utils.db_connection import get_db_connection
from app.subsystems.geocoding_service import GeocodingService


class CityService:

    @staticmethod
    def add_city(name):
        """
        Add city if it does not exist.
        Save latitude & longitude using Geocoding API.
        """
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 🔹 Check if city already exists
        cursor.execute(
            "SELECT id FROM cities WHERE name = %s",
            (name,)
        )
        city = cursor.fetchone()

        if city:
            cursor.close()
            conn.close()
            return city["id"]

        # 🔹 Get latitude & longitude
        geo = GeocodingService()
        lat, lon = geo.get_coordinates(name)

        # 🔹 Insert city with lat/lon
        cursor.execute(
            """
            INSERT INTO cities (name, latitude, longitude)
            VALUES (%s, %s, %s)
            """,
            (name, lat, lon)
        )
        conn.commit()

        city_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return city_id

    @staticmethod
    def get_city_by_id(city_id: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM cities WHERE id = %s",
            (city_id,)
        )
        city = cursor.fetchone()

        cursor.close()
        conn.close()
        return city

    @staticmethod
    def get_city_by_name(name):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM cities WHERE name = %s",
            (name,)
        )
        city = cursor.fetchone()

        cursor.close()
        conn.close()
        return city

    @staticmethod
    def get_all_cities():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM cities")
        cities = cursor.fetchall()

        cursor.close()
        conn.close()
        return cities
