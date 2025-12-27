# app/controllers/favorites_controller.py
from flask import Blueprint, redirect, session, flash
from app.service.favorite_city_service import FavoriteCityService

fav_bp = Blueprint("favorites", __name__, url_prefix="/favorites")

@fav_bp.route("/remove/<int:city_id>", methods=["POST"])
def remove(city_id):
    uid = session.get("user_id")
    if not uid:
        return redirect("/login")
    FavoriteCityService.remove_favorite(uid, city_id)
    flash("City removed from favourites")
    return redirect("/dashboard")