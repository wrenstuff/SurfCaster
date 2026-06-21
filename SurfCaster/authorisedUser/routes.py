# authorisedUser/routes.py

# library imports
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

# local imports
from db_models import Users, FlaggedScans, ApprovedScans
from extensions import db, get_reviews, scan_history, flag_scan, get_scan_history, get_review_history, wait_time, getDate
import models.Baelin as Baelin
import url_extractor as ex
from torch import torch
import joblib

# blueprint creation
user_routes = Blueprint('user_routes', __name__)

# route definitions
# Dashboard
@user_routes.route('/')
def home():
    if session.get('role') != 'user':
        return "Unauthorized", 403
    history = get_scan_history()

    return render_template('dashboard.html', history=history)

# URL Scanner
@user_routes.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method ==  'GET':
        if session.get('role') != 'user':
            return "Unauthorized", 403

        return render_template('scan.html')
    if request.method == 'POST':
        url = request.form.get('url')

        # turn url into features then convert to tensor
        url_features = ex.extract_url_features(url)

        checkpoint = torch.load(
            'SurfCaster/models/Baelin_checkpoint.pth', map_location="cpu"
        )

        scaler = joblib.load('SurfCaster/models/Baelin_scaler.pkl')

        input_size = checkpoint["input_size"]
        feature_columns = checkpoint["feature_columns"]
        threshold = checkpoint["threshold"]

        model = Baelin.Baelin(input_size)
        model.load_state_dict(checkpoint["model_state_dict"])
        model.eval()

        prediction = model.predict(
            url_features,
            scaler=scaler,
            feature_columns=feature_columns
        )

        phishing_probability = prediction["phishing_probability"] * 100

        session['last_scanned_url'] = url
        session["phishing_probability"] = phishing_probability

        session["last_scan_result"] = phishing_probability

        scan_history(
            url,
            phishing_probability
        )

        wait_time()

        return redirect(url_for('user_routes.scan'))
    
@user_routes.route('/flag_scan_route', methods=['POST'])
def flag_scan_route():
    if session.get('role') != 'user':
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

    return redirect(url_for('user_routes.scan'))

# Scan History
@user_routes.route('/history')
def history():
    if session.get('role') != 'user':
        return "Unauthorized", 403
    history = get_scan_history()

    return render_template('scan_history.html', history=history)

# Account
@user_routes.route('/account') # possibly change to username?
def account():
    if session.get('role') != 'user':
        return "Unauthorized", 403
    
    date = getDate()

    return render_template('account.html', date=date)

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


