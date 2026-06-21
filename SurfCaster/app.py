# app.py

# library imports
from os import link

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from sqlalchemy import text
from argon2 import PasswordHasher

# internal imports
# Uncomment when routes have been added
from admin.routes import admin_routes
from reviewer.routes import reviewer_routes
from authorisedUser.routes import user_routes
from unauthorisedUser.routes import unauthorised_user_routes
from auth.routes import auth_routes
from extensions import db
from datetime import datetime


ph = PasswordHasher()

# app creation and blueprint registration


app = Flask(__name__)
app.secret_key = "supersecretkey"

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
    
    with db.engine.begin() as conn:
        result = conn.execute(text("""
            SELECT 1 FROM users
            WHERE username = :username
            LIMIT 1
        """), {"username": "admin"}).fetchone()
        joindate = datetime.now().strftime("%Y%m%d")

        #DELETE THIS BEFORE LAUNCHING
        if not result:
            hashed_pw = ph.hash("admin123")
            conn.execute(text("""
                INSERT INTO users (username, email, password, role, joindate)
                VALUES (:username, :email, :password, :role, :joindate)
            """), {
                "username": "admin",
                "email": "admin@admin",
                "password": hashed_pw,
                "role": "admin",
                "joindate": joindate
            })


# run the app
if __name__ == "__main__":
    app.run(debug=True)