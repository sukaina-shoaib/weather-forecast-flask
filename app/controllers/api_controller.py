# app/controllers/api_controller.py
from flask import Blueprint, request, jsonify
from app.facade.weather_facade import WeatherFacade
from app.service.favorite_city_service import FavoriteCityService
from flask_jwt_extended import jwt_required, get_jwt_identity

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

@api_bp.route("/weather/current")
@jwt_required()          # remove decorator if you do not use JWT
def current():
    city = request.args.get("city")
    if not city:
        return jsonify(error="city required"), 400
    facade = WeatherFacade()
    data = facade.get_current_weather(city)
    return jsonify(data)

@api_bp.route("/user/favorites")
@jwt_required()
def favorites():
    uid = get_jwt_identity()
    rows = FavoriteCityService.get_user_favorites(uid)
    return jsonify(rows)