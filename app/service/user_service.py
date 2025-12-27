# app/services/user_service.py

from app.utils.db_connection import get_db_connection

class UserService:

    @staticmethod
    def create_user(name, email, password):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO users (name, email, password)
        VALUES (%s, %s, %s)
        """
        values = (name, email, password)
        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        conn.close()
        return True

    @staticmethod
    def get_user_by_email(email):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()
        return user

    @staticmethod
    def validate_login(email, password):
        user = UserService.get_user_by_email(email)
        if user and user["password"] == password:
            return user
        return None

    @staticmethod
    def get_user_by_id(user_id: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    @staticmethod
    def update_profile(uid, name, password=None):
        conn = get_db_connection()
        cur = conn.cursor()
        if password:
            cur.execute("UPDATE users SET name=%s, password=%s WHERE id=%s", (name, password, uid))
        else:
            cur.execute("UPDATE users SET name=%s WHERE id=%s", (name, uid))
        conn.commit();
        cur.close();
        conn.close()

    # UserService
    @staticmethod
    def get_all_users():
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, name, email FROM users")
        rows = cur.fetchall()
        cur.close();
        conn.close()
        return rows

    def authenticate(self, email: str, password: str):
        """Return user dict if credentials OK, else None."""
        return self.validate_login(email, password)