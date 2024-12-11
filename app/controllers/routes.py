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
            # Redirect to the dashboard
            return render_template("dashboard.html")
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
            # Redirect to the dashboard
            return render_template("dashboard.html")
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
def upload():
    if request.method == "POST":  # Handle file uploads
        if "file" not in request.files:
            # Return error response if no file part
            return jsonify({"error": "No file part"}), 400

        file = request.files["file"]  # Get the uploaded file
        if file.filename == "":
            # Return error response if no file selected
            return jsonify({"error": "No selected file"}), 400

        if file:
            filename = secure_filename(file.filename)  # Secure the filename
            upload_folder = current_app.config["UPLOAD_FOLDER"]

            # Create upload folder if it doesn't exist
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)  # Save the file to the server

            # Return JSON response with file name
            return jsonify({"message": "File uploaded successfully!", "fileName": filename}), 200

    elif request.method == "GET":  # Render the upload page
        return render_template("upload.html")


@main.route("/process-churn", methods=["POST"])
def process_churn():
    file = request.files.get("file")
    target_column = request.form.get("target_column")

    if not file or not target_column:
        return jsonify({"error": "File and target column are required"}), 400

    filename = secure_filename(file.filename)
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    file_path = os.path.join(upload_folder, filename)

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file.save(file_path)

    try:
        churn_result = FileProcessor.UploadFile(file_path, target_column)
        return jsonify({"message": "Churn processed successfully", "result": churn_result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/preview-data", methods=["POST"])
def preview_data():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        # Read file into a pandas DataFrame
        if file.filename.endswith(".csv"):
            data = pd.read_csv(file)
        elif file.filename.endswith(".xlsx"):
            data = pd.read_excel(file)
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        # Get headers and first few rows
        headers = list(data.columns)
        rows = data.head(10).to_dict(orient="records")

        return jsonify({"headers": headers, "rows": rows}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
