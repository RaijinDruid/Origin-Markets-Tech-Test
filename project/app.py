import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app(config_obj):
    """
        Create and configure an instance of the Flask application.

        ARGUMENTS
        ----------------------
        config_obj:
            type: dict
            description: pass in a dict with environment variables

    """
    app = Flask(__name__)
    if config_obj:
        app.config.from_mapping(config_obj)
        with app.app_context():
            from project.database import Base, engine
            from project import models
            models.Base.metadata.create_all(bind=engine)
            from project.routes import bond_bp, user_bp, token_bp
            app.register_blueprint(bond_bp)
            app.register_blueprint(user_bp)
            app.register_blueprint(token_bp)
        return app
    else:
        raise RuntimeError("Please provide a configuration for flask application")
