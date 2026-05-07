# authorisedUser/routes.py

# library imports
from flask import Blueprint, render_template

# blueprint creation
user_routes = Blueprint('user_routes', __name__)

# route definitions
# Dashboard
@user_routes.route('/')
def home():
    return render_template('dashboard.html')

# URL Scanner
@user_routes.route('/scan')
def scan():
    return render_template('scan.html')

# Scan History
@user_routes.route('/history')
def history():
    return render_template('scan_history.html')

# Account
@user_routes.route('/account') # possibly change to username?
def account():
    return "Authorised User Account"

# Settings
@user_routes.route('/settings')
def settings():
    return "Authorised User Settings"

# Support
@user_routes.route('/support')
def support():
    return "Authorised User Support"


