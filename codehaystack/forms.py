from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (
    StringField,
    TextAreaField,
    EmailField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    BooleanField,
    HiddenField,
    SubmitField,
)
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class SignUpForm(FlaskForm):
    """Registration form class"""

    username = StringField("Username", validators=[DataRequired()])
    full_name = StringField("Full Name")
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password should be more than 8 characters"),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", "Passwords do not match")],
    )

    submit = SubmitField("Create New Account")


class LogInForm(FlaskForm):
    """Signin form class"""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    next = HiddenField()

    login = SubmitField("Log In")


class UserProfileForm(FlaskForm):
    """User Profile Form class"""

    username = StringField("Username", validators=[DataRequired()])
    role = SelectField("Role", validators=[DataRequired()], validate_choice=False)
    full_name = StringField("Full Name")
    email = EmailField("Email", validators=[DataRequired(), Email()])
    website = StringField("Website")
    twitter_username = StringField("Twitter Username (without @)")
    linkedin_url = StringField("LinkedIn URL")
    bio = TextAreaField("Bio")
    profile_image = FileField("Profile Image")
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password should be more than 8 characters"),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", "Passwords do not match")],
    )

    submit = SubmitField("Save User")


class UserProfileUpdateForm(FlaskForm):
    """User Profile Form class"""

    username = StringField("Username")
    role = SelectField("Role", validators=[DataRequired()], validate_choice=False)
    full_name = StringField("Full Name")
    email = EmailField("Email", validators=[DataRequired(), Email()])
    website = StringField("Website")
    twitter_username = StringField("Twitter Username (without @)")
    linkedin_url = StringField("LinkedIn URL")
    bio = TextAreaField("Bio")
    profile_image = FileField("Profile Image")
    password = PasswordField(
        "Set New Password",
        validators=[
            Optional(),
            Length(min=8, message="Password should be more than 8 characters"),
        ],
    )
    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[EqualTo("password", "Passwords do not match")],
    )

    submit = SubmitField("Update User")


class PostArticleForm(FlaskForm):
    """Create or Edit Post form class"""

    title = StringField("Title", validators=[DataRequired()])
    slug = StringField("Slug")
    description = TextAreaField("Meta Description")
    categories = SelectMultipleField(
        "Categories", validators=[DataRequired()], validate_choice=False
    )
    tags = SelectMultipleField("Tags", validate_choice=False)
    content = CKEditorField("Content", validators=[DataRequired()])

    featured_image = FileField("Featured Image")

    status = SelectField(
        "Post Status", choices=["Draft", "Publish"], validators=[DataRequired()]
    )

    submit = SubmitField("Submit Post")


class TermForm(FlaskForm):
    """Create or Edit Terms and Taxonomy"""

    name = StringField("Name", validators=[DataRequired()])
    description = CKEditorField("Description")
    slug = StringField("Slug")

    submit = SubmitField("Add New Term")
