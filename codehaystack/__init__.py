from flask import Flask


def create_app():
    """Create and configure a new flask application"""
    app = Flask(__name__, instance_relative_config=True)

    # create a new database instance
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    # supress warnings
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize and bind db and migration to app
    from .extensions import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # import and register blueprints
    from .routes.main import main
    app.register_blueprint(main)

    return app
