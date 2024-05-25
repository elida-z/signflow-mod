import os
import sys
from flask import Flask

# Ensure the root of your project is in the Python path
# Assuming this script is inside a subfolder of the project directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Flask application initialization with absolute imports
from config.settings import Config  # Configurations from a settings module
from routes.views import register_routes  # Import routes

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configurations from the Config class

    register_routes(app)  # Register routes with the app

    # Additional initialization logic can be placed here

    return app
