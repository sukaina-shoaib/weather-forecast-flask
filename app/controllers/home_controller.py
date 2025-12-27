from flask import Blueprint, render_template, session, redirect
from app.service.favorite_city_service import FavoriteCityService
from app.service.notification_service import NotificationService

home_bp = Blueprint("home", __name__)
favorite_service = FavoriteCityService()
notification_service = NotificationService()


@home_bp.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    favorites = favorite_service.get_user_favorites(user_id)
    notifications = notification_service.get_notifications(user_id)

    return render_template("home/dashboard.html",
                           favourites=favorites,  # ← use British spelling
                           notifications=notifications)

@home_bp.route("/")
def landing():
    """Any visitor hits '/' --> login screen."""
    return redirect("/login")