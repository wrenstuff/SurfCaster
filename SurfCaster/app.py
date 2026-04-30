# app.py

# library imports
from flask import Flask

# internal imports
# Uncomment when routes have been added
#from admin.routes import admin_routes
from reviewer.routes import reviewer_routes
from authorisedUser.routes import user_routes
from unauthorisedUser.routes import unauthorised_user_routes

# app creation and blueprint registration
app = Flask(__name__)

#app.register_blueprint(admin_routes, url_prefix='/admin')
app.register_blueprint(reviewer_routes, url_prefix='/reviewer')
app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(unauthorised_user_routes, url_prefix='/unauth')

# run the app
if __name__ == "__main__":
    app.run(debug=True)