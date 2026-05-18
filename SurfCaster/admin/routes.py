# admin/routes.py

# library imports
from flask import Blueprint, redirect, render_template, request, session, url_for
from user_model import Users
from extensions import db

# blueprint creation
admin_routes = Blueprint('admin_routes', __name__)

# route definitions
# Dashboard
@admin_routes.route('/')
def home():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    return render_template('dashboard.html')

# URL Scanner
@admin_routes.route('/scan')
def scan():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    return render_template('scan.html')

# Scan History
@admin_routes.route('/history')
def history():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    return render_template('scan_history.html')

# Account
@admin_routes.route('/account') # possibly change to username?
def account():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    return render_template('account.html')

# Settings
@admin_routes.route('/settings')
def settings():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    return render_template('settings.html')

# Support
@admin_routes.route('/support')
def support():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    return render_template('support.html')

# Review Queue
@admin_routes.route('/queue')
def queue():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    return render_template('review-queue.html')

# Review History
@admin_routes.route('/reviews')
def reviews():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    return render_template('review-history.html')

# User Management
@admin_routes.route('/users')
def users():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    
    all_users = Users.query.all()
    return render_template('user-management.html', users=all_users)

@admin_routes.route('/update_role', methods=['POST'])
def update_role():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    
    username = request.form.get('username')
    new_role = request.form.get('role')
    user = Users.query.filter_by(username=username).first()
    if user:
        user.role = new_role
        db.session.commit()

    return redirect(url_for('admin_routes.users'))

# Model Management
@admin_routes.route('/models')
def models():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    return render_template('model-management.html')

# Database Management
@admin_routes.route('/database')
def database():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    return render_template('database-management.html')

# Audit Logs
@admin_routes.route('/logs')
def logs():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    return render_template('audit-logs.html')