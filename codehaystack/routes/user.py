import os

from flask import Blueprint, render_template, flash, redirect, url_for, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename

from ..models.user import User, Role
from ..extensions import db
from ..forms import UserProfileForm, UserProfileUpdateForm
from ..functions import allowed_image, unique_filename

# New Blueprint instance
user = Blueprint("user", __name__, url_prefix="/dashboard/users")


@user.route("/")
@login_required
def users():
    """Route to show all users in database"""

    # get all users from database
    users = User.query.all()

    return render_template("dashboard/users.html", users=users)


@user.route("/create", methods=["GET", "POST"])
@login_required
def create_user():
    """Route to create new user"""

    # get new instance of `UserProfileForm()`
    user_form = UserProfileForm()

    # populate the role field
    user_form.role.choices = [
        role.name for role in Role.query.order_by(Role.name).all()
    ]

    # validate and process form
    if user_form.validate_on_submit():
        # get submitted username, email, and profile_image
        username = user_form.username.data
        email = user_form.email.data
        profile_image = user_form.profile_image.data

        if User.query.filter_by(username=username).first():
            # username exists
            flash("Username already in use!", "danger")
            return render_template("dashboard/create_user.html", form=user_form)

        elif User.query.filter_by(email=email).first():
            # email exists
            flash("Email already in use", "danger")
            return render_template("dashboard/create_user.html", form=user_form)

        elif profile_image and not allowed_image(profile_image.filename):
            # email format is not allowed
            flash("Profile image can only be jpg, png, gif, or webp formats!", "danger")
            return render_template("dashboard/create_user.html", form=user_form)

        # manual validations passed ======

        # if profile image is uploaded, save image to server
        if profile_image:
            # get secure_filename from uploaded image
            profile_image_filename = secure_filename(profile_image.filename)

            # create `unique_filename`
            unique_profile_filename = unique_filename(profile_image_filename)

            # set filepath
            filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"], unique_profile_filename
            )

            # upload the image with unique filename
            profile_image.save(filepath)

        else:
            # no image was uploaded
            unique_profile_filename = None

        # creat new instance of User
        new_user = User(
            username=username,
            full_name=user_form.full_name.data,
            email=email,
            bio=user_form.bio.data,
            profile_image_path=unique_profile_filename,
            website=user_form.website.data,
            twitter_username=user_form.twitter_username.data,
            linkedin_url=user_form.linkedin_url.data,
        )

        # set password_hash for new user
        new_user.set_password(user_form.password.data)

        # set role for new user
        new_user.role = Role.query.filter_by(name=user_form.role.data).first()

        # save new user to database
        db.session.add(new_user)
        db.session.commit()

        # success feedback
        flash("New user created successfully!", "success")

        return redirect(url_for("user.users"))

    else:
        # validation not passed
        for field, errors in user_form.errors.items():
            for error in errors:
                flash(f"{field.title().replace('_', ' ')}: {error}", "danger")

    return render_template("dashboard/create_user.html", form=user_form)


@user.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_user(id):
    """Route to edit user based on `id`"""

    # get user from database based on `id`
    user = User.query.filter_by(id=id).first()

    # get new instance of `UserProfileUpdateForm()`
    user_form = UserProfileUpdateForm()

    # populate the role field
    user_form.role.choices = [
        role.name for role in Role.query.order_by(Role.name).all()
    ]

    # validate and process form
    if user_form.validate_on_submit():
        # get submitted email, profile_image, and new password
        email = user_form.email.data
        profile_image = user_form.profile_image.data
        new_password = user_form.password.data

        # check if email is existing
        existing_email = User.query.filter_by(email=email).first()

        if existing_email and email != user.email:
            flash("Email already in use!", "danger")
            return render_template("dashboard/edit_user.html", form=user_form)

        elif profile_image and not allowed_image(profile_image.filename):
            # email format is not allowed
            flash("Profile image can only be jpg, png, gif, or webp formats!", "danger")
            return render_template("dashboard/edit_user.html", form=user_form)

        # manual validations passed ======

        # if profile image is uploaded, save image to server
        if profile_image:
            # get secure_filename from uploaded image
            profile_image_filename = secure_filename(profile_image.filename)

            # create `unique_filename`
            unique_profile_filename = unique_filename(profile_image_filename)

            # set filepath
            filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"], unique_profile_filename
            )

            # upload the image with unique filename
            profile_image.save(filepath)

        else:
            # no image was uploaded
            unique_profile_filename = user.profile_image_path

        # update the user
        user.full_name = user_form.full_name.data
        user.email = email
        user.bio = user_form.bio.data
        user.profile_image_path = unique_profile_filename
        user.website = user_form.website.data
        user.twitter_username = user_form.twitter_username.data
        user.linkedin_url = user_form.linkedin_url.data
        user.role = Role.query.filter_by(name=user_form.role.data).first()

        if new_password:
            user.set_password(new_password)

        # update user record in database
        db.session.add(user)
        db.session.commit()

        # success feedback
        flash("User updated successfully!", "success")

        return redirect(url_for("user.users"))

    else:
        # validation not passed
        for field, errors in user_form.errors.items():
            for error in errors:
                flash(f"{field.title().replace('_', ' ')}: {error}", "danger")

    # populate edit form
    user_form.username.data = user.username
    user_form.full_name.data = user.full_name
    user_form.email.data = user.email
    user_form.bio.data = user.bio
    user_form.website.data = user.website
    user_form.twitter_username.data = user.twitter_username
    user_form.linkedin_url.data = user.linkedin_url
    user_form.role.process_data(user.role.name)

    return render_template("dashboard/edit_user.html", user=user, form=user_form)


@user.route("/delete/<int:id>")
@login_required
def delete_user(id):
    """Route to delete user from database based on `id`"""

    # get the user based on id
    user = User.query.filter_by(id=id).first()

    # commit changes to database
    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully!", "success")

    return redirect(url_for("user.users"))
