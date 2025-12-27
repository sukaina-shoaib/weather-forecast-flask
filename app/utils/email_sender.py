from flask import current_app
from flask_mail import Message
from app import mail          # imported from __init__.py

def send_email(to_address: str, subject: str, body: str) -> None:
    """
    Send an e-mail to one recipient.
    """
    if not to_address:
        return

    msg = Message(
        subject=subject,
        recipients=[to_address],
        body=body,
        sender=current_app.config['MAIL_USERNAME']
    )
    mail.send(msg)