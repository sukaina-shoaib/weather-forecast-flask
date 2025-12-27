# app/service/alert_service.py

from app.utils.db_connection import get_db_connection
from app.observer.weather_alert_subject import WeatherAlertSubject
from app.observer.dashboard_observer import DashboardObserver
from app.observer.email_observer import EmailObserver
from app.service.notification_service import NotificationService


class AlertService:

    # -----------------------------
    # CREATE ALERT
    # -----------------------------
    @staticmethod
    def create_alert(user_id, city_id, alert_type, threshold):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO alerts (user_id, city_id, alert_type, threshold_value)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, city_id, alert_type, threshold)
        )
        conn.commit()
        cur.close()
        conn.close()

    # -----------------------------
    # DELETE ALERT
    # -----------------------------
    @staticmethod
    def delete_alert(alert_id, user_id):
        conn = get_db_connection()
        cur = conn.cursor()

        # 🔴 hide notifications of this alert
        NotificationService.clear_by_alert(alert_id)

        cur.execute(
            "DELETE FROM alerts WHERE id = %s AND user_id = %s",
            (alert_id, user_id)
        )

        conn.commit()
        cur.close()
        conn.close()

    # -----------------------------
    # GET USER ALERTS
    # -----------------------------
    @staticmethod
    def get_user_alerts(user_id):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT a.id, a.alert_type, a.threshold_value, c.name AS city_name
            FROM alerts a
            JOIN cities c ON a.city_id = c.id
            WHERE a.user_id = %s
            ORDER BY a.id DESC
        """, (user_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    # -----------------------------
    # ALERTS FOR CITY
    # -----------------------------
    @staticmethod
    def get_user_alerts_for_city(user_id, city_name):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT a.*
            FROM alerts a
            JOIN cities c ON a.city_id = c.id
            WHERE a.user_id = %s AND c.name = %s
        """, (user_id, city_name))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    # -----------------------------
    # CHECK & FIRE ALERTS
    # -----------------------------
    @staticmethod
    def check_and_trigger_alerts(user_id, city_name, weather):

        alerts = AlertService.get_user_alerts_for_city(user_id, city_name)

        subject = WeatherAlertSubject()
        subject.attach(DashboardObserver())
        subject.attach(EmailObserver())

        for alert in alerts:

            # ❌ already fired → skip
            if NotificationService.was_already_fired(user_id, alert["id"]):
                continue

            triggered = False
            msg = ""

            if alert["alert_type"] == "weather_contains":
                if alert["threshold_value"].lower() in weather["condition"].lower():
                    triggered = True
                    msg = f"Alert #{alert['id']}: {city_name} has {weather['condition']}"

            elif alert["alert_type"] == "temperature_ge":
                if weather["temperature"] >= float(alert["threshold_value"]):
                    triggered = True
                    msg = f"Alert #{alert['id']}: {city_name} temperature {weather['temperature']}°C"

            elif alert["alert_type"] == "temperature_le":
                if weather["temperature"] <= float(alert["threshold_value"]):
                    triggered = True
                    msg = f"Alert #{alert['id']}: {city_name} temperature {weather['temperature']}°C"

            elif alert["alert_type"] == "wind_ge":
                if weather["wind_speed"] >= float(alert["threshold_value"]):
                    triggered = True
                    msg = f"Alert #{alert['id']}: Wind speed {weather['wind_speed']} km/h"

            if triggered:
                subject.notify(user_id, msg)
