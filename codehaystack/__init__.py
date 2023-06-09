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

    # initialize and bind `db`, `migration`, `login_manager`, `ckeditor` to app
    from .extensions import db, migrate, login_manager, ckeditor

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    ckeditor.init_app(app)

    # Insert admin and user Role if not available
    from .models.user import Role

    @app.before_first_request
    def add_roles():
        # confirm user roles in database before first app request
        user_roles = Role.query.all()

        if not user_roles:
            admin_role = Role(name="admin")
            editor_role = Role(name="editor")
            user_role = Role(name="user")

            db.session.add(admin_role)
            db.session.add(editor_role)
            db.session.add(user_role)
            db.session.commit()

    # default login view
    login_manager.login_view = "auth.login"

    # get user object with user's id
    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == user_id).first()

    # import and register blueprints
    from .routes.main import main
    from .routes.auth import auth
    from .routes.post import post
    from .routes.category import category
    from .routes.tag import tag
    from .routes.dashboard import dashboard
    from .routes.user import user
    from .routes.file import file

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(post)
    app.register_blueprint(category)
    app.register_blueprint(tag)
    app.register_blueprint(dashboard)
    app.register_blueprint(file)
    app.register_blueprint(user)

    return app
