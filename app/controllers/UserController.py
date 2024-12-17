from flask import json, jsonify, render_template
from app.models import UserModel


class UserController:
    """
    User Logic for Login, Register, Password reset, Search, and Update user information
    _summary_

    Returns:
        _type_: _description_
    """

    @staticmethod
    def index():
        return render_template("index.html")

    # Login logice
    @staticmethod
    def login(email, password):
        # get the user from the database
        user = UserModel.query.filter_by(email=email).first()
        # found the user
        if user:
            # check the password
            if user.password == password:
                return "Login successful"
            else:
                return jsonify({"error": "Incorrect password"}), 400
        else:
            return jsonify({"error": "User not found"}), 400

    # Register Logice for flask
    @staticmethod
    def register(name, email, password):
        # create a new user
        user = UserModel(name=name, email=email, password=password)
        # add the user to the database
        UserModel.add(user)
        return jsonify({"message": "User registered successfully"}), 201

    # Password reset logic
    @staticmethod
    def reset_password(email, new_password):
        # get the user from the database
        user = UserModel.query.filter_by(email=email).first()
        # found the user
        if user:
            # update the password
            user.password = new_password
            # add the user to the database
            UserModel.add(user)
            return jsonify({"message": "Password reset successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 400

    # Update user information
    @staticmethod
    def update_user(user_id, name, email, password):
        # get the user from the database
        user = UserModel.query.get(user_id)
        # found the user
        if user:
            # update the user information
            user.name = name
            user.email = email
            user.password = password
            # add the user to the database
            UserModel.add(user)
            return jsonify({"message": "User updated successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 400

    # Search user information
    @staticmethod
    def search_user(name):
        # get the user from the database
        user = UserModel.query.filter_by(name=name).first()
        # found the user
        if user:
            return json.dumps(
                user.to_dict()
            )  # convert the user to a dictionary and return it as a JSON user
        else:
            return jsonify({"error": "User not found"}), 400
