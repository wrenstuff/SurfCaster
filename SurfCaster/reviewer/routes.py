# reviewer/routes.py

# library imports
from flask import Blueprint

# blueprint creation
reviewer_routes = Blueprint('reviewer_routes', __name__)

# route definitions
# Dashboard
@reviewer_routes.route('/')
def home():
    return "Reviewer Dashboard"

# URL Scanner
@reviewer_routes.route('/scan')
def scan():
    return "Reviewer URL Scan"

# Scan History
@reviewer_routes.route('/history')
def history():
    return "Reviewer Scan History"

# Account
@reviewer_routes.route('/account') # possibly change to username?
def account():
    return "Reviewer Account"

# Settings
@reviewer_routes.route('/settings')
def settings():
    return "Reviewer Settings"

# Support
@reviewer_routes.route('/support')
def support():
    return "Reviewer Support"

# Review Queue
@reviewer_routes.route('/queue')
def queue():
    return "Reviewer Review Queue"

# Review History
@reviewer_routes.route('/reviews')
def reviews():
    return "Reviewer Review History"

#logout
@reviewer_routes.route('/logout')
def logout():
    return "Reviewer Logout"
