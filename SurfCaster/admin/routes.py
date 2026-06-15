# admin/routes.py

# library imports
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

# local imports
from db_models import Users, FlaggedScans, ApprovedScans
from extensions import db, get_reviews, scan_history, create_scan_id, flag_scan, get_scan_history, get_review_history, wait_time, getDate
import models.Baelin as Baelin
import url_extractor as ex

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
@admin_routes.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method ==  'GET':
        if session.get('role') != 'admin':
            return "Unauthorized", 403

        return render_template('scan.html')
    if request.method == 'POST':
        url = request.form.get('url')

        # turn url into features then convert to tensor
        features = ex.extract_url_features(url)

        model = Baelin.Baelin()

        session['last_scanned_url'] = url

        last_scan_result = model.predict(features) * 100

        session['last_scan_result'] = last_scan_result

        scan_history(url, last_scan_result)

        wait_time()

        return redirect(url_for('admin_routes.scan'))

@admin_routes.route('/flag_scan_route', methods=['POST'])
def flag_scan_route():
    if session.get('role') != 'admin':
        return "Unauthorized", 403

    # hopefully second time is the charm. 
    # I already did this but it didn't commit (˃̣̣̥ᯅ˂̣̣̥)
    url = session.get('last_scanned_url')
    status = request.form.get('flag')


    if session.get('last_scan_result') <= 100/3:
        flag = 'safe'
    elif session.get('last_scan_result') <= 200/3:
        flag = 'unsure'
    else:
        flag = 'unsafe'

    to_send = flag_scan(url, flag, status)

    flagged_scan = FlaggedScans(
        scan_id=to_send['scan_id'],
        user_id=to_send['user_id'],
        url=to_send['url'],
        flag=to_send['flag'],
        status=to_send['status']
    )
    db.session.add(flagged_scan)
    db.session.commit()

    return redirect(url_for('admin_routes.scan'))


# Scan History
@admin_routes.route('/history')
def history():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    
    history = get_scan_history()

    return render_template('scan_history.html', history=history)

# Account
@admin_routes.route('/account') # possibly change to username?
def account():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    
    date = getDate()

    return render_template('account.html', date=date)

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
    reviews = get_reviews()
    return render_template('review-queue.html', reviews=reviews)

@admin_routes.route('/review_scan', methods=['POST'])
def review_scan():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    
    scan_id = request.form.get('scan_id')
    action = request.form.get('action')
    if action not in ['approve', 'reject']:
        flash("Invalid action", "error")
        return redirect(url_for('admin_routes.queue'))
    else:
        if action == 'approve':
            status = True if request.form.get('flag') == 'Safe' else False

    to_db = ApprovedScans(
        scan_id=scan_id,
        reviewer_id=session.get('user_id'),
        url=request.form.get('url'),
        status=status
    )
    db.session.add(to_db)
    db.session.commit()

    to_remove = FlaggedScans.query.filter_by(scan_id=scan_id).first()
    db.session.delete(to_remove)
    db.session.commit()

    return redirect(url_for('admin_routes.queue'))


# Review History
@admin_routes.route('/reviews')
def reviews():
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    
    scans = get_review_history()

    return render_template('review-history.html', scans=scans)

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