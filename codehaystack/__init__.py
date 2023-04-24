import os
from flask import Flask


def create_app():
    """Create and configure a new flask application"""
    app = Flask(__name__, instance_relative_config=True)

    # load config file in `config.py` file
    # create `config.py` from `config_sample.py` template
    from . import config

    app.config.from_mapping(config.config)

    # ensure the upload folder exists
    try:
        os.makedirs(app.config["UPLOAD_FOLDER"])
    except OSError:
        pass

    # initialize and bind `db`, `migration` and `login_manager` to app
    from .extensions import db, migrate, login_manager

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # default login view
    login_manager.login_view = "profile.login"

    # get user object with user's id
    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == user_id).first()

    # import and register blueprints
    from .routes.main import main
    from .routes.profile import profile
    from .routes.post import post
    from .routes.term import term
    from .routes.dashboard import dashboard
    from .routes.file import file

    app.register_blueprint(main)
    app.register_blueprint(profile)
    app.register_blueprint(post)
    app.register_blueprint(term)
    app.register_blueprint(dashboard)
    app.register_blueprint(file)

    return app
