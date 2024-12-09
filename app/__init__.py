from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()


def create_app():
    # Set custom template folder
    app = Flask(__name__, template_folder="views")

    app.config["UPLOAD_FOLDER"] = "path/to/upload/folder"

    # Load configuration
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)

    # Register controllers
    with app.app_context():
        db.create_all()  # Create database tables
        from app.controllers import register_routes

        register_routes(app)

    return app
