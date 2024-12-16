import io
import os
import uuid
import base64
from flask import (
    request,
    jsonify,
    send_file,
    session,
    url_for,
    redirect,
    Blueprint,
    current_app,
    render_template,
)
import pandas as pd
from .controllers.UploadController import (
    FileProcessor,
) 
from werkzeug.utils import (
    secure_filename,
) 
from .controllers.user_controller import (
    UserController,
) 

from app.models.UserModel import UserModel
from app.models.DataModel import DataModel

from .middleware.CaptchaMiddleware import CaptchaMiddleware


# Define a Blueprint for modular application structure and routing
main = Blueprint("main", __name__)

# Initialize CaptchaMiddleware
captcha_middleware = CaptchaMiddleware(main)

# Route to serve CAPTCHA image
@main.route('/captcha')
def serve_captcha_image():
    try:
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        UPLOAD_FOLDER = os.path.join(BASE_DIR, 'upload_folder')  # Absolute path
        current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        captcha_id = str(uuid.uuid4())  # Generate a unique ID for CAPTCHA
        session['captcha_id'] = captcha_id  # Store the ID for validation

        # Create CAPTCHA folder inside UPLOAD_FOLDER
        captcha_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], "captcha")
        os.makedirs(captcha_folder, exist_ok=True)

        # Generate CAPTCHA image using middleware
        captcha_text = session.get('captcha')
        captcha_base64 = captcha_middleware.generate_captcha_image(captcha_text)
        if not captcha_base64:
            raise ValueError("CAPTCHA generation failed: No data returned")

        # Save the CAPTCHA image
        captcha_image_path = os.path.join(captcha_folder, f"{captcha_id}.png")
        with open(captcha_image_path, "wb") as img_file:
            img_file.write(base64.b64decode(captcha_base64))

        if os.path.exists(captcha_image_path):
            return send_file(captcha_image_path, mimetype="image/png")
        else:
            raise FileNotFoundError("CAPTCHA image file not found")

    except Exception as e:
        current_app.logger.error(f"Error serving CAPTCHA image: {e}")
        return 'Error generating CAPTCHA image', 500

# Delete CAPTCHA image after use
def delete_captcha_image(captcha_id):
    try:
        captcha_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], "captcha")
        captcha_image_path = os.path.join(captcha_folder, f"{captcha_id}.png")
        
        if os.path.exists(captcha_image_path):
            os.remove(captcha_image_path)
    except Exception as e:
        current_app.logger.error(f"Error deleting CAPTCHA image: {e}")


# Login route: Handles both GET and POST requests for user login
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":  # If a form is submitted
        # Extract email, password, and CAPTCHA from the form
        email = request.form.get("email")
        password = request.form.get("password")
        user_captcha = request.form.get("captcha")  # Get CAPTCHA entered by the user

        # Validate CAPTCHA
        stored_captcha_id = session.get("captcha")
        
        if not stored_captcha_id:
            return render_template("login.html", error="CAPTCHA expired. Please refresh.")

        # Compare user input with stored CAPTCHA
        if user_captcha != stored_captcha_id:
            # Delete CAPTCHA image and generate a new one
            delete_captcha_image(stored_captcha_id)
            return render_template("login.html", error="Incorrect CAPTCHA. Try again.")

        # Validate credentials (using the UserModel)
        user = UserModel.find_by_email(email)
        if user and user.verify_password(password):
            # Store session data for logged-in user
            session["logged_in"] = True
            session["user"] = user.email
            session["user_id"] = user.id
            
            
            # Delete CAPTCHA image after successful login
            delete_captcha_image(stored_captcha_id)
            
            return redirect(url_for("main.dashboard"))
        else:
            return render_template("login.html", error="Invalid email or password")

    # Render the login page for GET request
    return render_template("login.html")

# Register route: Handles both GET and POST requests for user registration
# Register route with CAPTCHA validation
@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user_captcha = request.form.get("captcha")

        # Validate CAPTCHA
        stored_captcha_id = session.get("captcha_id")
        if not stored_captcha_id:
            # Delete CAPTCHA image and generate a new one
            delete_captcha_image(stored_captcha_id)
            return render_template("register.html", error="CAPTCHA expired. Please refresh.")

        if user_captcha != stored_captcha_id:
            # Delete CAPTCHA image and generate a new one
            delete_captcha_image(stored_captcha_id)
            return render_template("register.html", error="Incorrect CAPTCHA. Try again.")

        # Check if user already exists
        if UserModel.find_by_email(email):
            # Delete CAPTCHA image and generate a new one
            delete_captcha_image(stored_captcha_id)
            return render_template("register.html", error="Email already exists")

        # Create and save new user
        new_user = UserModel(email=email, password=password)
        new_user.save()

        # Delete CAPTCHA image after successful registration
        delete_captcha_image(stored_captcha_id)

        return redirect(url_for("main.login"))

    return render_template("register.html")

# Logout route: Handles POST requests to log the user out
@main.route("/logout", methods=["POST"])
def logout():
    # Remove the logged-in session variable
    session.pop("logged_in", None)
    # Redirect the user to the homepage
    return render_template("main.login")

# Dashboard route: Renders the user dashboard
@main.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("main.login"))
    return render_template("dashboard.html", user=session.get("user"))

# Get data user has uploaded
@main.route("/api/data", methods=["GET"])
def get_data():
    # Retrieve the user's info from the session
    user_id = session.get("user_id")  # Make sure the session key matches the one used during login
    
    if not user_id:
        # Redirect to login if the user session is not available
        return redirect(url_for("main.login"))

    # Query the database for data associated with the user
    data = DataModel.query.filter_by(user_id=user_id).all()
    
    # If no data is found, inform the user
    if not data:
        return jsonify({"message": "No data found. Please upload a file."}), 200
    
    
    # Convert the data to a JSON-friendly format
    data_list = [
        {"id": d.id, "fileName": d.file_name, "filePath": d.file_path, "user": d.user_id} for d in data
    ]
    
    # Return the data as JSON
    return jsonify(data_list)


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
            
            # Retrieve the user ID from the session
            user_id = session.get("user_id")  # Ensure that the session key is 'user_id'
            
            if not user_id:
                # User should be logged in
                return jsonify({"error": "User not logged in"}), 401

            # Save file details to the database
            file_name = filename
            data = DataModel(user_id=user_id, file_name=file_name, file_path=file_path)
            # Save data to the database
            data.save()

            # Return JSON response with file name and message
            return jsonify({"message": "File uploaded successfully!", "fileName": filename}), 200

    elif request.method == "GET":
        return render_template("upload.html")

# Read file route: Handles file reading
@main.route("/api/read-file", methods=["POST"])
def read_file():
    # Get file_id and user_id from the form or request
    file_id = request.form.get('file_id')
    user_id = request.form.get('user_id')  # Assuming user_id is passed in the request (e.g., from session or token)
    
    if not file_id or not user_id:
        return jsonify({"error": "File ID and user ID are required."}), 400
    
    # Query the file from the database
    file = DataModel.query.filter_by(id=file_id).first()

    # Check if the file exists
    if not file:
        return jsonify({"error": "File not found."}), 404
    
    # Check if the logged-in user is the owner of the file
    if file.user_id != int(user_id):  # Assuming file.user_id links to the User model
        return jsonify({"error": "You are not the owner of this file."}), 403
    
    # File exists and belongs to the user, so proceed to read the file
    file_path = file.file_path  # Assuming the file path is stored in the file model
    
    try:
        # Read the file using pandas
        df = pd.read_csv(file_path)
        print(df.head(10))
        # Convert the dataframe to a dictionary format for easy display in the frontend
        data = jsonify(df.to_dict(orient='records'))
        # print(data)
        return data
    except Exception as e:
        return jsonify({"error": f"Error reading file: {str(e)}"}), 500

# Process churn route: Handles churn processing
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
