# unauthorisedUser/routes.py

# library imports
from flask import Blueprint

# blueprint creation
unauthorised_user_routes = Blueprint('unauthorised_user_routes', __name__)

# route definitions
# Dashboard
@unauthorised_user_routes.route('/')
def home():
    return "Unauthorised User Dashboard"

# URL Scanner
@unauthorised_user_routes.route('/scan')
def scan():
    return "Unauthorised User URL Scan"

# Settings
@unauthorised_user_routes.route('/settings')
def settings():
    return "Unauthorised User Settings"

# Support
@unauthorised_user_routes.route('/support')
def support():
    return "Unauthorised User Support"