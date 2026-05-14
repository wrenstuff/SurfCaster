# app.py

# library imports
from os import link

from flask import Flask, session
from pathlib import Path

# internal imports
# Uncomment when routes have been added
from admin.routes import admin_routes
from reviewer.routes import reviewer_routes
from authorisedUser.routes import user_routes
from unauthorisedUser.routes import unauthorised_user_routes
from auth.routes import auth_routes

# app creation and blueprint registration

file_path = Path(__file__).parent / "static" / "images" / "cat.png"
if file_path.is_file():
    app = Flask(__name__)
    app.secret_key = "supersecretkey"

app.register_blueprint(admin_routes, url_prefix='/admin')
app.register_blueprint(reviewer_routes, url_prefix='/reviewer')
app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(unauthorised_user_routes, url_prefix='/unauth')
app.register_blueprint(auth_routes, url_prefix='/')
# run the app
if __name__ == "__main__":
    app.run(debug=True)