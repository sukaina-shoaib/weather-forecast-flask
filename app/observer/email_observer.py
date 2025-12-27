from app.observer.observer_interface import Observer
from app.utils.email_sender import send_email
from app.service.user_service import UserService   # already exists

class EmailObserver(Observer):
    def update(self, user_id: int, message: str) -> None:
        user = UserService.get_user_by_id(user_id)   # new helper – see below
        if not user:
            return

        send_email(
            to_address=user['email'],
            subject="Weather Alert",
            body=message
        )