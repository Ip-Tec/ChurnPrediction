# This file allows the directory to be treated as a Python package.

from app.routes import main
from .UploadController import FileProcessor
from .UserController import UserController

# Function to register controllers


def register_routes(app):
    app.register_blueprint(main)
