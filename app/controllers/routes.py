import os  # Provides functions to interact with the operating system
from flask import (
    request,
    jsonify,
    session,
    Blueprint,
    current_app,
    render_template,
)  # Flask modules for app structure and handling HTTP requests/responses
from .UploadController import (
    FileProcessor,
)  # Custom controller for file upload handling
from werkzeug.utils import (
    secure_filename,
)  # Utility to secure filenames for file uploads
from .user_controller import (
    UserController,
)  # Custom controllers for user and upload functionality

# Define a Blueprint for modular application structure and routing
main = Blueprint("main", __name__)


# Home route: Renders the homepage
@main.route("/")
def home():
    # Render the homepage using the 'home.html' template
    return render_template("home.html")


# Login route: Handles both GET and POST requests for user login
@main.route("/login", methods=["GET", "POST"])
def login():
    # Show the login page or handle login logic
    UserController.index()  # Call the UserController index method (logic not shown here)
    if request.method == "POST":  # If a form is submitted
        # Extract email and password from the form
        email = request.form["email"]
        password = request.form["password"]
        # Validate credentials (in this case, hardcoded check)
        if email == "admin" and password == "admin":
            session["logged_in"] = True  # Mark the user as logged in
            return render_template("dashboard.html")  # Redirect to the dashboard
        else:
            return "Login failed"  # Handle invalid credentials
    # Render the login page if it's a GET request
    return render_template("login.html")


# Register route: Handles both GET and POST requests for user registration
@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":  # If a form is submitted
        # Extract email and password from the form
        email = request.form["email"]
        password = request.form["password"]
        # Validate credentials (same hardcoded check as login)
        if email == "admin" and password == "admin":
            session["logged_in"] = True  # Mark the user as logged in
            return render_template("dashboard.html")  # Redirect to the dashboard
        else:
            return "Login failed"  # Handle invalid credentials
    # Render the registration page if it's a GET request
    return render_template("register.html")


# Logout route: Handles POST requests to log the user out
@main.route("/logout", methods=["POST"])
def logout():
    # Remove the logged-in session variable
    session.pop("logged_in", None)
    # Redirect the user to the homepage
    return render_template("home.html")


# Dashboard route: Renders the user dashboard
@main.route("/dashboard")
def dashboard():
    # Render the dashboard page using the 'dashboard.html' template
    return render_template("dashboard.html")


# File upload route: Handles file uploads via GET and POST
@main.route("/upload", methods=["GET", "POST"])
def Upload():
    if request.method == "POST":  # If a file upload form is submitted
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400  # Return an error response
        file = request.files["file"]  # Extract the file from the request
        if file.filename == "":
            return (
                jsonify({"error": "No selected file"}),
                400,
            )  # Return an error response
        if file:
            filename = secure_filename(file.filename)  # Secure the filename
            upload_folder = current_app.config["UPLOAD_FOLDER"]
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)  # Save the file

            # Pass the file path to FileProcessor
            processing_result = FileProcessor.UploadFile(file_path)

            return (
                jsonify(
                    {
                        "message": "File uploaded successfully!",
                        "result": processing_result,
                    }
                ),
                200,
            )
    elif request.method == "GET":
        return render_template("upload.html")
