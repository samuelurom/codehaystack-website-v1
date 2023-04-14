from flask import Flask


def create_app():
    """Create and configure a new flask application"""
    app = Flask(__name__, instance_relative_config=True)

    # create a new database instance
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    # supress warnings
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # CSRF Secrete Key
    app.config["SECRET_KEY"] = "c8BXNC%ieGtj^XNa5Ow6UbuaZeAz%J3PBBY8oVUtNW625o#n2I"

    # Initialize and bind db and migration to app
    from .extensions import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # import and register blueprints
    from .routes.main import main
    from .routes.account import account
    from .routes.create_post import create_post

    app.register_blueprint(main)
    app.register_blueprint(account)
    app.register_blueprint(create_post)

    return app
