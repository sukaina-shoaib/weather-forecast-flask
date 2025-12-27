# app/controllers/notification_controller.py
from flask import Blueprint, redirect, session, render_template, flash

from app.service import notification_service
from app.service.notification_service import NotificationService

notif_bp = Blueprint("notifications", __name__, url_prefix="/notifications")

@notif_bp.route("")
def inbox():
    uid = session.get("user_id")
    if not uid:
        return redirect("/login")
    rows = NotificationService().get_notifications(uid)
    return render_template("notifications/inbox.html", notifications=rows)

@notif_bp.route("/read/<int:nid>", methods=["POST"])
def mark_read(nid):
    NotificationService().mark_as_read(nid)
    return redirect("/notifications")

@notif_bp.route("/read_all", methods=["POST"])
def mark_all_read():
    uid = session.get("user_id")
    if not uid:
        return redirect("/login")
    NotificationService().mark_all_as_read(uid)
    return redirect("/notifications")

@notif_bp.route("/delete_all", methods=["POST"])   # <-- route exists
def delete_all():                                  # <-- function name
    uid = session.get("user_id")
    if not uid:
        return redirect("/login")
    NotificationService.delete_all(uid)            # your soft-delete
    flash("All notifications deleted")
    return redirect("/notifications")

@notif_bp.route("/delete/<int:nid>", methods=["POST"])
def delete_single(nid):
    NotificationService().hide_notification(nid)
    flash("Notification hidden")
    return redirect("/notifications")

# @notif_bp.route("/delete/<int:nid>", methods=["POST"])
# def delete_single(nid):
#     NotificationService().hide_notification(nid)
#     flash("Notification hidden")
#     return redirect("/notifications")