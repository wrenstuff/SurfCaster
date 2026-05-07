# admin/routes.py

# library imports
from flask import Blueprint, render_template

# blueprint creation
admin_routes = Blueprint('admin_routes', __name__)

# route definitions
# Dashboard
@admin_routes.route('/')
def home():
    return render_template('dashboard.html')

# URL Scanner
@admin_routes.route('/scan')
def scan():
    return render_template('scan.html')

# Scan History
@admin_routes.route('/history')
def history():
    return render_template('scan_history.html')

# Account
@admin_routes.route('/account') # possibly change to username?
def account():
    return render_template('account.html')

# Settings
@admin_routes.route('/settings')
def settings():
    return render_template('settings.html')

# Support
@admin_routes.route('/support')
def support():
    return "Admin Support"

# Review Queue
@admin_routes.route('/queue')
def queue():
    return "Admin Review Queue"

# Review History
@admin_routes.route('/reviews')
def reviews():
    return "Admin Review History"

# User Management
@admin_routes.route('/users')
def users():
    return "Admin User Management"

# Model Management
@admin_routes.route('/models')
def models():
    return "Admin Model Management"

# Database Management
@admin_routes.route('/database')
def database():
    return "Admin Database Management"

# Audit Logs
@admin_routes.route('/logs')
def logs():
    return "Admin Audit Logs"