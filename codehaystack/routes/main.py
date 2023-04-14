from flask import Blueprint

main = Blueprint("main", __name__)


@main.route('/')
def index():
    return '<h1>Hello, CodeHaystack</h1>'
