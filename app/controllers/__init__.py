# This file allows the directory to be treated as a Python package.

from .routes import main

# Function to register controllers


def register_routes(app):
    app.register_blueprint(main)
