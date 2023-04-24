from flask import current_app
import uuid


def unique_filename(filename):
    # generate random string
    random_string = uuid.uuid4().hex

    # get the file extension
    name = filename.rsplit('.', 1)[0]
    ext = filename.rsplit('.', 1)[1].lower()

    # generate unique filename
    unique_filename = f"{name}_{random_string}.{ext}"

    return unique_filename


def allowed_image(filename):
    """Function to check if image format is allowed"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower(
        ) in current_app.config['ALLOWED_IMAGE_EXTENSIONS']
