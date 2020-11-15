import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app(config_obj):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    if config_obj:
        app.config.from_mapping(config_obj)
        print(app.config)
        with app.app_context():
            from project.database import Base, engine
            from project import models
            models.Base.metadata.create_all(bind=engine)
            from project.routes import bond_bp, user_bp
            app.register_blueprint(bond_bp)
            app.register_blueprint(user_bp)
        return app
    else:
        raise RuntimeError("Please provide a configuration for flask application")

