from flask import Blueprint, request, render_template, redirect, session
from datetime import datetime, timedelta

from app.facade.weather_facade import WeatherFacade
from app.service.weather_log_service import WeatherLogService
from app.service.alert_service import AlertService
from app.service.favorite_city_service import FavoriteCityService
from app.service.city_service import CityService

weather_bp = Blueprint("weather", __name__)

facade = WeatherFacade()
log_service = WeatherLogService()
alert_service = AlertService()
favorite_service = FavoriteCityService()


@weather_bp.route("/weather", methods=["GET"])
def get_weather_page():
    return render_template("weather/search_city.html")


@weather_bp.route("/weather/result", methods=["GET", "POST"])
def weather_result():
    city_name = request.form.get("city") or request.args.get("city")

    if not city_name:
        return redirect("/weather")

    # -------------------------------------------------
    # 1. SAVE CITY + LAT/LON (HANDLE INVALID CITY)
    # -------------------------------------------------
    try:
        city_id = CityService.add_city(city_name)
    except ValueError:
        # 🚫 City not found → show friendly page
        return render_template(
            "errors/city_not_found.html",
            city=city_name
        )

    # -------------------------------------------------
    # 2. FETCH WEATHER DATA (SAFE)
    # -------------------------------------------------
    try:
        current = facade.get_current_weather(city_name)
        forecast = facade.get_7day_forecast(city_name)
    except Exception:
        return render_template(
            "errors/city_not_found.html",
            city=city_name
        )

    # -------------------------------------------------
    # 3. NEXT 6 HOURS
    # -------------------------------------------------
    hourly = []
    for i, f in enumerate(forecast[:6]):
        hourly.append({
            "time": (datetime.now() + timedelta(hours=i * 3)).strftime("%H:%M"),
            "temp": int(f["temperature"]),
            "condition": f["condition"]
        })

    # -------------------------------------------------
    # 4. 7-DAY FORECAST
    # -------------------------------------------------
    daily = []
    days = ["Today", "Fri", "Sat", "Sun", "Mon", "Tue", "Wed"]
    chunks = len(forecast) // 8 if len(forecast) >= 8 else 1

    for i in range(7):
        idx = i * chunks if i * chunks < len(forecast) else -1
        f = forecast[idx]

        daily.append({
            "day": days[i],
            "high": int(f["temperature"]),
            "low": int(f["temperature"]) - 2,
            "wind": int(f.get("wind_speed", 0)),
            "condition": f["condition"]
        })

    # -------------------------------------------------
    # 5. CHART DATA
    # -------------------------------------------------
    chart_labels = [d["day"] for d in daily]
    chart_temps = [d["high"] for d in daily]
    chart_wind = [d["wind"] for d in daily]

    # -------------------------------------------------
    # 6. FAVORITES
    # -------------------------------------------------
    user_id = session.get("user_id")
    favorites = FavoriteCityService.get_user_favorites(user_id) if user_id else []
    city_in_favs = any(f["name"].lower() == city_name.lower() for f in favorites)

    # -------------------------------------------------
    # 7. LOG WEATHER + ALERT CHECK
    # -------------------------------------------------
    if user_id:
        log_service.create_log(
            user_id,
            city_name,
            current["temperature"],
            current["condition"]
        )

        alert_messages = alert_service.check_and_trigger_alerts(
            user_id,
            city_name,
            {
                "temperature": current["temperature"],
                "wind_speed": current.get("wind_speed", 0),
                "condition": current["condition"]
            }
        )
    else:
        alert_messages = []

    # -------------------------------------------------
    # 8. RENDER PAGE
    # -------------------------------------------------
    return render_template(
        "weather/weather_result.html",
        city=city_name,
        current=current,
        hourly=hourly,
        daily=daily,
        chart_labels=chart_labels,
        chart_temps=chart_temps,
        chart_wind=chart_wind,
        city_in_favs=city_in_favs,
        btn_temp=int(current["temperature"]),
        btn_wind=int(current.get("wind_speed", 0)),
        alerts=alert_messages
    )


@weather_bp.route("/weather/add_favorite/<city>")
def add_favorite(city):
    user_id = session.get("user_id")
    if user_id:
        favorite_service.add_favorite_city(user_id, city)
    return redirect("/dashboard")
