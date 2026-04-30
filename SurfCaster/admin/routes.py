# admin/routes.py

# library imports
from flask import Blueprint

# blueprint creation
admin_routes = Blueprint('admin_routes', __name__)

# route definitions
# Dashboard
# admin/routes.py@admin_routes.route('/')
def home():
    return "Admin Dashboard"

# URL Scanner
@admin_routes.route('/scan')
def scan():
    return "Admin URL Scan"

# Scan History
@admin_routes.route('/history')
def history():
    return "Admin Scan History"

# Account
@admin_routes.route('/account') # possibly change to username?
def account():
    return "Admin Account"

# Settings
@admin_routes.route('/settings')
def settings():
    return "Admin Settings"

# Support
@admin_routes.route('/support')
def support():
    return "Admin Support"

#logout
@admin_routes.route('/logout')
def logout():
    return "Admin Logout"