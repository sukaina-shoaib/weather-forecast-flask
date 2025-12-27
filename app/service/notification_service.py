# app/service/notification_service.py

from app.utils.db_connection import get_db_connection


class NotificationService:

    def create_notification(self, user_id, message):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO notifications (user_id, message) VALUES (%s, %s)",
            (user_id, message)
        )
        conn.commit()
        cur.close()
        conn.close()

    def get_notifications(self, user_id):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT * FROM notifications
            WHERE user_id = %s
            AND message NOT LIKE '[hidden]%%'
            ORDER BY created_at DESC
            """,
            (user_id,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @staticmethod
    def was_already_fired(user_id, alert_id, minutes=120):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT 1 FROM notifications
            WHERE user_id = %s
            AND message LIKE %s
            """,
            (user_id, f'%Alert #{alert_id}%')
        )
        found = cur.fetchone()
        cur.close()
        conn.close()
        return found is not None

    @staticmethod
    def clear_by_alert(alert_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE notifications
            SET message = CONCAT('[hidden]', message), is_read = 1
            WHERE message LIKE %s
            """,
            (f'%Alert #{alert_id}%',)
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def delete_all(user_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE notifications
            SET message = CONCAT('[hidden]', message), is_read = 1
            WHERE user_id = %s
            """,
            (user_id,)
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def mark_as_read(nid):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE notifications SET is_read = 1 WHERE id = %s",
            (nid,)
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def mark_all_as_read(uid):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE notifications SET is_read = 1 WHERE user_id = %s",
            (uid,)
        )
        conn.commit()
        cur.close()
        conn.close()
