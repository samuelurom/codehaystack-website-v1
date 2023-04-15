from flask import (Blueprint, render_template,
                   request, redirect, url_for, flash)

from ..forms import SignUpForm
from ..models.post import Post
from ..models.user import User
from ..extensions import db

account = Blueprint("account", __name__, url_prefix="/dashboard")


@account.route("/signup", methods=["GET", "POST"])
def signup():
    # create new instance of sign up form
    signup_form = SignUpForm()

    # form validation and processing
    if signup_form.validate_on_submit():
        # get submitted username and email
        username = signup_form.username.data
        email = signup_form.email.data

        # check for existing username and email
        # create new user if validation is passed
        if User.query.filter_by(email=email).first():
            flash("Email already in use!")

        elif User.query.filter_by(username=username).first():
            flash("Username already in use!")

        else:
            # create new user object
            new_user = User(
                email=email,
                username=username,
                full_name=signup_form.full_name.data
            )

            # set user password hash
            new_user.set_password(signup_form.password.data)

            # commit
            db.session.add(new_user)
            db.session.commit()

            flash("Your account has been created!", "success")

            return redirect(url_for("account.signup"))
    else:
        # validation not passed
        for field, errors in signup_form.errors.items():
            for error in errors:
                flash(f"{field.title().replace('_', ' ')}: {error}", "error")
                print(field)

    return render_template("/dashboard/signup.html", form=signup_form)
