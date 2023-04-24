import os

config = {
    "SECRET_KEY": "",
    "SQLALCHEMY_DATABASE_URI": "sqlite:///db.sqlite3",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "UPLOAD_FOLDER": os.path.join(os.getcwd(), "uploads"),
    "ALLOWED_IMAGE_EXTENSIONS": {"png", "jpg", "jpeg", "gif", "webp"},
    "MAX_CONTENT_LENGTH": 6 * 1024 * 1024,
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 465,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "",
    "MAIL_PASSWORD": "",
}
