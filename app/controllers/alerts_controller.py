from flask import Blueprint, request, redirect, session, flash, render_template
from app.service.alert_service import AlertService
from app.service.city_service import CityService

alerts_bp = Blueprint("alerts", __name__, url_prefix="/alerts")


@alerts_bp.route("")
def index():
    uid = session.get("user_id")
    if not uid:
        return redirect("/login")

    alerts = AlertService.get_user_alerts(uid)
    return render_template("alerts/index.html", alerts=alerts)


@alerts_bp.route("/create", methods=["GET"])
def create_form():
    uid = session.get("user_id")
    if not uid:
        return redirect("/login")

    cities = CityService.get_all_cities()
    return render_template("alerts/create.html", cities=cities)


@alerts_bp.route("/create", methods=["POST"])
def create():
    uid = session.get("user_id")
    if not uid:
        return redirect("/login")

    city_id = request.form.get("city_id")
    alert_type = request.form.get("alert_type")

    if alert_type == "weather_contains":
        threshold = request.form.get("threshold_text")
    else:
        threshold = request.form.get("threshold_number")

    if not threshold:
        flash("Threshold value required")
        return redirect("/alerts/create")

    AlertService.create_alert(uid, city_id, alert_type, threshold)
    flash("Alert created successfully")
    return redirect("/alerts")


@alerts_bp.route("/delete/<int:alert_id>", methods=["POST"])
def delete(alert_id):
    uid = session.get("user_id")
    AlertService.delete_alert(alert_id, uid)
    flash("Alert removed")
    return redirect("/alerts")
