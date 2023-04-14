from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileSize, FileAllowed
from wtforms import (StringField, TextAreaField, EmailField,
                     PasswordField, SelectField, SubmitField)
from wtforms.validators import DataRequired, Email, EqualTo


class SignUp(FlaskForm):
    """Registration form class"""
    username = StringField("Username", validators=[DataRequired()])
    full_name = StringField("Full Name")
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo('password', "Passwords do not match")
    ])
    submit = SubmitField("Create New Account")


class UserProfile(FlaskForm):
    """User Profile Form class"""
    username = StringField("Username", validators=[DataRequired()])
    full_name = StringField("Full Name")
    email = EmailField("Email", validators=[DataRequired()])
    bio = TextAreaField("Bio")
    update = SubmitField("Update Profile")


class ChangePassword(FlaskForm):
    """Change User Password"""
    old_password = PasswordField("Old Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class PostArticle(FlaskForm):
    """Create or Edit Post form class"""
    title = StringField("Title", validators=[DataRequired()])
    url = StringField("URL")
    description = TextAreaField("Meta Description")
    content = TextAreaField("Content", validators=[DataRequired()])
    featured_image = FileField("Featured Image", validators=[
        FileSize(max_size=1000000),
        FileAllowed(["jpg", "png", "webp"], "Image files only!")
    ])
    status = SelectField("Post Status", choices=[
                         "", "Draft", "Publish"], validators=[DataRequired()])
    submit = SubmitField("Submit Post")
