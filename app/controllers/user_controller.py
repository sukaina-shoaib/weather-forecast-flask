# app/controllers/user_controller.py
from flask import Blueprint, render_template, request, redirect, session, flash
from app.service.user_service import UserService

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/profile")
def profile():
    uid = session.get("user_id")
    if not uid:
        return redirect("/login")
    user = UserService.get_user_by_id(uid)
    return render_template("user/profile.html", user=user)

@user_bp.route("/profile/update", methods=["POST"])
def update():
    uid = session.get("user_id")
    if not uid:
        return redirect("/login")
    name = request.form.get("name")
    password = request.form.get("password") or None
    UserService.update_profile(uid, name, password)
    flash("Profile updated")
    return redirect("/user/profile")