# authorisedUser/routes.py

# library imports
from flask import Blueprint, render_template, session

# blueprint creation
user_routes = Blueprint('user_routes', __name__)

# route definitions
# Dashboard
@user_routes.route('/')
def home():
    if session.get('role') != 'user':
        return "Unauthorized", 403
    return render_template('dashboard.html')

# URL Scanner
@user_routes.route('/scan')
def scan():
    if session.get('role') != 'user':
        return "Unauthorized", 403
    return render_template('scan.html')

# Scan History
@user_routes.route('/history')
def history():
    if session.get('role') != 'user':
        return "Unauthorized", 403
    return render_template('scan_history.html')

# Account
@user_routes.route('/account') # possibly change to username?
def account():
    if session.get('role') != 'user':
        return "Unauthorized", 403
    return render_template('account.html')

# Settings
@user_routes.route('/settings')
def settings():
    if session.get('role') != 'user':
        return "Unauthorized", 403
    return render_template('settings.html')

# Support
@user_routes.route('/support')
def support():
    if session.get('role') != 'user':
        return "Unauthorized", 403
    return render_template('support.html')


