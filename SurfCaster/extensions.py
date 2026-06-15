import os

from flask import json, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime
import time
import calendar

db = SQLAlchemy()

def wait_time():
    time.sleep(.5)

def load_json_file(path, default):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, 'w') as f:
            json.dump(default, f)
        return default
    
    with open(path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return default

def save_json_file(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)

def scan_history(url, last_scan_result):
    history_path = 'scan_history.json'
    settings_path = 'user_settings.json'

    history = load_json_file(history_path, [])
    settings = load_json_file(settings_path, {"full_scan_history": False})

    full_scan_history = settings.get('full_scan_history', False)

    history.insert(0, {"date": datetime.now().isoformat(), "url": url, "last_scan_result": last_scan_result})

    if not full_scan_history:
        history = history[:10]

    save_json_file(history_path, history)

def create_scan_id():
    # get the current date and time
    scan_id = str(datetime.now().strftime("%Y%m%d%H%M%S"))

    #get the user ID to 8 digits
    try:
        user_id = str(session.get('user_id', '0'))
    except RuntimeError:
        user_id = '0'
    scan_id += user_id.zfill(8)
    return scan_id

def flag_scan(url, flag, status):
    scan_id = create_scan_id()
    user_id = session.get('user_id', None)
    if user_id is None:
        return "Unauthorized", 403
    
    scan = {
        'scan_id': scan_id,
        'user_id': user_id,
        'url': url,
        'flag': flag,
        'status': status
    }

    return scan

def get_scan_history():
    if not os.path.exists('scan_history.json'):
        return []
    history_path = 'scan_history.json'
    history = load_json_file(history_path, [])
    return history

def get_reviews():
    result = db.session.execute(text("SELECT * FROM flagged_scans"))
    rows = result.fetchall()

    reviews = {}

    for row in rows:
        scan_id = row[1]
        username_result = db.session.execute(text("SELECT username FROM users WHERE id = :user_id"), {"user_id": row[2]}).fetchone()
        reviews[scan_id] = {
            'scan_id': row[1],
            'username': username_result[0] if username_result else None,
            'url': row[3],
            'flag': row[4],
            'status': row[5]
        }
    return reviews

def get_review_history():
    if session.get('role') == "admin":
        result = db.session.execute(text("SELECT * FROM approved_scans"))
    elif session.get('role') == "reviewer":
        result = db.session.execute(text("SELECT * FROM approved_scans WHERE reviewer_id = :user_id"), {"user_id": session.get('user_id')})
    else:
        return []
    rows = result.fetchall()

    reviews = []

    for row in rows:
        scan_id = row[1]
        username_result = db.session.execute(text("SELECT username FROM users WHERE id = :user_id"), {"user_id": row[2]}).fetchone()
        reviews.append({
            'scan_id': row[1],
            'url': row[3],
            'status': row[4],
            'reviewer': username_result[0] if username_result else None
        })
    return reviews

def getDate():
    full = str(session.get('join_date'))

    y = 0
    year = ''
    month = ''
    day = ''
    for x in full:
        if y < 4:
            year += x
        elif y < 6:
            month += x
        else:
            day += x
        
        y += 1

    month = int(month)
    month = calendar.month_name[month]

    date = day + " " + month + " " + year

    return date