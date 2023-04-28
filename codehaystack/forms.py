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
from wtforms.validators import DataRequired, Email, EqualTo, Length


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
    full_name = StringField("Full Name")
    email = EmailField("Email", validators=[DataRequired()])
    bio = TextAreaField("Bio")

    update = SubmitField("Update Profile")


class ChangePasswordForm(FlaskForm):
    """Change User Password"""

    old_password = PasswordField("Old Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])

    submit = SubmitField("Submit")


class PostArticleForm(FlaskForm):
    """Create or Edit Post form class"""

    title = StringField("Title", validators=[DataRequired()])
    slug = StringField("Slug")
    description = TextAreaField("Meta Description")
    categories = SelectMultipleField(
        "Categories", validators=[DataRequired()], validate_choice=False
    )
    tags = SelectMultipleField("Tags", validate_choice=False)
    content = TextAreaField("Content", validators=[DataRequired()])

    featured_image = FileField("Featured Image")

    status = SelectField(
        "Post Status", choices=["Draft", "Publish"], validators=[DataRequired()]
    )

    submit = SubmitField("Submit Post")


class TermForm(FlaskForm):
    """Create or Edit Terms and Taxonomy"""

    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description")
    slug = StringField("Slug")

    submit = SubmitField("Add New Term")
