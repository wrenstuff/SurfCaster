# reviewer/routes.py

# library imports
from flask import Blueprint, render_template, session

# blueprint creation
reviewer_routes = Blueprint('reviewer_routes', __name__)

# route definitions
# Dashboard
@reviewer_routes.route('/')
def home():
    if session.get('role') != 'reviewer':
        return "Unauthorized", 403
    return render_template('dashboard.html')

# URL Scanner
@reviewer_routes.route('/scan')
def scan():
    if session.get('role') != 'reviewer':
        return "Unauthorized", 403
    return render_template('scan.html')

# Scan History
@reviewer_routes.route('/history')
def history():
    if session.get('role') != 'reviewer':
        return "Unauthorized", 403
    return render_template('scan_history.html')

# Account
@reviewer_routes.route('/account') # possibly change to username?
def account():
    if session.get('role') != 'reviewer':
        return "Unauthorized", 403
    return render_template('account.html')

# Settings
@reviewer_routes.route('/settings')
def settings():
    if session.get('role') != 'reviewer':
        return "Unauthorized", 403
    return render_template('settings.html')

# Support
@reviewer_routes.route('/support')
def support():
    if session.get('role') != 'reviewer':
        return "Unauthorized", 403
    return render_template('support.html')

# Review Queue
@reviewer_routes.route('/queue')
def queue():
    if session.get('role') != 'reviewer':
        return "Unauthorized", 403
    return render_template('review-queue.html')

# Review History
@reviewer_routes.route('/reviews')
def reviews():
    if session.get('role') != 'reviewer':
        return "Unauthorized", 403
    return render_template('review-history.html')

