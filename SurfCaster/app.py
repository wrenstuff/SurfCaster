# app.py

# library imports
from os import link
import os

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from sqlalchemy import text
from argon2 import PasswordHasher

# internal imports
# Uncomment when routes have been added
from db_models import Users
from admin.routes import admin_routes
from reviewer.routes import reviewer_routes
from authorisedUser.routes import user_routes
from unauthorisedUser.routes import unauthorised_user_routes
from auth.routes import auth_routes
from extensions import db
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
ph = PasswordHasher()

# app creation and blueprint registration


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SurfCaster.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(admin_routes, url_prefix='/admin')
app.register_blueprint(reviewer_routes, url_prefix='/reviewer')
app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(unauthorised_user_routes, url_prefix='/unauth')
app.register_blueprint(auth_routes, url_prefix='/')

db.init_app(app)
with app.app_context():
    db.create_all()
    
    admin = Users.query.filter_by(username='admin').first()

    if not admin:
        hashed_password = ph.hash('admin123')

        admin = Users(username='admin',
        email='admin@admin',
        password=hashed_password,
        role='admin',
        joindate=datetime.now().strftime("%Y%m%d"))

    db.session.add(admin)
    db.session.commit()

#flash hook for security headers (clears session data on logout and prevents caching of sensitive pages)
@app.after_request
def add_security_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# run the app
if __name__ == "__main__":
    app.run(debug=True)