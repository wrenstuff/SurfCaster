# app.py

# library imports
from flask import Flask

# internal imports
from admin import routes as admin_routes
from reviewer import routes as reviewer_routes
from authorisedUser import routes as user_routes
from unauthorisedUser import routes as unauthorised_user_routes

# app creation and blueprint registration
app = Flask(__name__)
app.register_blueprint(admin_routes)
app.register_blueprint(reviewer_routes)
app.register_blueprint(user_routes)
app.register_blueprint(unauthorised_user_routes)

# run the app
if __name__ == "__main__":
    app.run(debug=True)