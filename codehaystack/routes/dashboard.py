from flask import Blueprint, render_template
from flask_login import login_required

dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard.route("/")
@login_required
def dashbaord():
    return render_template("/dashboard/index.html")
