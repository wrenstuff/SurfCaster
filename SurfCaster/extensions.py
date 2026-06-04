import os

from flask import json, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

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

def flag_scan(url, flag):
    scan_id = create_scan_id()
    user_id = session.get('user_id', None)
    if user_id is None:
        return "Unauthorized", 403
    
    scan = {
        'scan_id': scan_id,
        'user_id': user_id,
        'url': url,
        'flag': flag
    }

    return scan