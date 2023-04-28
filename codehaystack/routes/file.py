from flask import Blueprint, current_app, send_from_directory

file = Blueprint("file", __name__)


@file.route("/uploads/<filename>")
def get_file(filename):
    """View to serve files in the `uploads` folder by filename"""
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
