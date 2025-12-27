# app/controllers/error_controller.py
from flask import Blueprint, render_template

err_bp = Blueprint("errors", __name__)

@err_bp.app_errorhandler(404)
def not_found(_):
    return render_template("errors/404.html"), 404

@err_bp.app_errorhandler(500)
def server_error(_):
    return render_template("errors/500.html"), 500