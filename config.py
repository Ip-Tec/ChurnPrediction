# config.py

import os


class Config:
    SECRET_KEY = "sumary_line"
    # SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key') | "sumary_line"

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', 'sqlite:///ChurnPrediction.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Debugging output
    print(f"SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}")


Config = Config
