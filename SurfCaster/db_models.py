# database configuration
from extensions import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='unauth')
    joindate = db.Column(db.String(14))

class FlaggedScans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.String(22), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    url = db.Column(db.String(2083), nullable=False)
    flag = db.Column(db.String(6), nullable=False)
    status = db.Column(db.String(6), nullable=False)

class ApprovedScans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.String(22), db.ForeignKey('flagged_scans.scan_id'), unique=True, nullable=False)
    url = db.Column(db.String(2083), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
