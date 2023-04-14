from flask import (Blueprint, render_template,
                   request, redirect, url_for, flash)

from ..forms import SignUp

account = Blueprint("account", __name__, url_prefix="/dashboard")


@account.route("/signup", methods=["GET", "POST"])
def signup():
    signup_form = SignUp()
    username = None

    if signup_form.validate_on_submit():
        email = signup_form.email.data
        username = signup_form.username.data
        full_name = signup_form.full_name.data
        password = signup_form.password.data

        return redirect(url_for("main.index"))

    return render_template("/dashboard/signup.html", form=signup_form, template_username=username)
