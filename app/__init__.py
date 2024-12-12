"""
This module initializes the Flask app and imports the necessary routes.
"""
from flask import Flask
# Initialize the Flask app here
app = Flask(__name__)
# Import routes after initializing the app to avoid cyclic import
# pylint: disable=C0413
from app import routes