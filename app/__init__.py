from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()


def create_app():
    # Set up the Flask app with a custom template folder
    app = Flask(__name__, template_folder="views")

    # Set upload folder for file uploads
    app.config["UPLOAD_FOLDER"] = "upload_folder"

    # Load configuration from config.py
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)

    # Import routes and models AFTER initializing the app and extensions
    from app.controllers import register_routes  # Import controllers
    from app.models import UserModel  # Import your models here

    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

    # Register routes
    register_routes(app)

    return app
