
from app import create_app

# Create Flask application instance using factory pattern
app = create_app()

if __name__ == "__main__":
    """Main application entry point.

    This script initializes and runs the Flask application.
    It creates the app instance and runs it in debug mode when executed directly.

    No arguments required.
    Returns: None
    """
    # Run the Flask application in debug mode
    app.run(debug=True)
