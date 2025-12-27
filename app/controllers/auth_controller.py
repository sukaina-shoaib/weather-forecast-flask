from flask import Blueprint, request, render_template, redirect, session, flash
from app.service.user_service import UserService

auth_bp = Blueprint("auth", __name__)
user_service = UserService()


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name     = request.form.get("name")
        email    = request.form.get("email")
        password = request.form.get("password")

        # ----  NEW : enforce 8-character minimum  ----
        if len(password) < 8:
            flash("Password must be at least 8 characters.")
            return render_template("auth/signup.html")

        UserService.create_user(name, email, password)
        flash("Account created – you can now log in.")
        return redirect("/login")

    return render_template("auth/signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email")
        password = request.form.get("password")

        if len(password) < 8:
            flash("Password must be at least 8 characters.")
            return render_template("auth/login.html")

        user = user_service.authenticate(email, password)
        if user:
            session["user_id"] = user["id"]
            return redirect("/dashboard")

        return render_template("auth/login.html",
                               error="Invalid email or password")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
