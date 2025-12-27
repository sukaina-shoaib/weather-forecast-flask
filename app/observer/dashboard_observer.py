from app.observer.observer_interface import Observer
from app.service.notification_service import NotificationService

class DashboardObserver(Observer):
    def update(self, user_id, message):
        print(f"[DASH-OBS] update called  user={user_id}  msg={message[:50]}")
        try:
            NotificationService().create_notification(user_id, message)
            print("[DASH-OBS] insert SUCCESS")
        except Exception as e:
            print(f"[DASH-OBS] insert FAILED  {e}")