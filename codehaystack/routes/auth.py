from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse

from ..forms import SignUpForm, LogInForm
from ..models.post import Post
from ..models.user import User, Role
from ..extensions import db

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/signup", methods=["GET", "POST"])
@login_required
def signup():
    """View for user signup"""

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
            flash("Email already in use!", "danger")

        # check if username exists
        elif User.query.filter_by(username=username).first():
            flash("Username already in use!", "danger")

        else:
            # create new user object
            new_user = User(
                email=email, username=username, full_name=signup_form.full_name.data
            )

            # set user password hash
            new_user.set_password(signup_form.password.data)

            # check if any user exists in database
            # if not set first user as admin
            all_users = User.query.all()

            if not all_users:
                # get admin `user` role from database
                user_role = Role.query.filter_by(name="admin").first()
            else:
                # get user `user` role from database
                user_role = Role.query.filter_by(name="user").first()

            # set user role
            new_user.role = user_role

            # commit
            db.session.add(new_user)
            db.session.commit()

            flash("Your account has been created!", "success")

            return redirect(url_for("auth.login"))
    else:
        # validation not passed
        for field, errors in signup_form.errors.items():
            for error in errors:
                flash(f"{field.title().replace('_', ' ')}: {error}", "danger")

    return render_template("auth/signup.html", form=signup_form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """View for user login"""

    # first check if current user is logged in
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    # crate instance of login form
    form = LogInForm()

    if form.validate_on_submit():
        # get user from database
        user = User.query.filter_by(username=form.username.data).first()

        # check if username is correct
        # redirect user to the `next` URL if it exists
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)

            flash("Logged in successfully!", "success")

            next_url = request.args.get("next")

            if not next_url or url_parse(next_url).netloc != "":
                next_url = url_for("dashboard.index")

            return redirect(next_url)

        else:
            flash("Invalid username or password!", "danger")

    # if validation fails, display the form with errors
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field.title().replace('_', ' ')}: {error}", "danger")

    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()

    flash("Logged out successfully!", "success")
    return redirect(url_for("auth.login"))
