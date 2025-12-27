# app/services/favorite_city_service.py

from app.utils.db_connection import get_db_connection

class FavoriteCityService:
    @staticmethod
    def remove_favorite(uid, city_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM favorites WHERE user_id=%s AND city_id=%s", (uid, city_id))
        conn.commit();
        cur.close();
        conn.close()

    @staticmethod
    def add_favorite_city(user_id, city_name: str):
        # 1. make sure city is in cities table
        from app.service.city_service import CityService
        city = CityService.get_city_by_name(city_name)
        if not city:
            city_id = CityService.add_city(city_name)
        else:
            city_id = city["id"]

        # 2. now insert into favorites
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO favorites (user_id, city_id) VALUES (%s, %s)",
            (user_id, city_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    # app/service/favorite_city_service.py

    @staticmethod
    def get_user_favorites(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
                SELECT fc.id  AS id,
                       c.id   AS city_id,
                       c.name AS name
                FROM favorites fc
                         JOIN cities c ON fc.city_id = c.id
                WHERE fc.user_id = %s \
                """
        cursor.execute(query, (user_id,))
        favorites = cursor.fetchall()

        cursor.close()
        conn.close()
        return favorites
        # ---- DEBUG ----
        # print(f"[DEBUG] favourites for user {user_id}: {favorites}")
