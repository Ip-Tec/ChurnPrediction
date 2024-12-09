from flask import render_template
from app.models import User


class UserController:
    @staticmethod
    def index():
        return render_template("index.html")

    # Login logice
    @staticmethod
    def login(email, password):
        # get the user from the database
        user = User.query.filter_by(email=email).first()
        # found the user
        if user:
            # check the password
            if user.password == password:
                return "Login successful"
            else:
                return "Login failed"
        else:
            return "User not found"

    # Register Logice for flask
    @staticmethod
    def register(name, email, password):
        # create a new user
        user = User(name=name, email=email, password=password)
        # add the user to the database
        User.add(user)
        return "User registered successfully"
