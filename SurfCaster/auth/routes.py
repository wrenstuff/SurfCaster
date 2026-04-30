from flask import Blueprint

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/')
def splash ():
    return "Welcome to SurfCaster! Please log in or register to continue."

# Login Page
@auth_routes.route('/login')
def login():
    print("Login attempt") # Debug statement
    if True: # Placeholder for actual login logic
        print("Login successful") # Debug statement
        return "dashboard//usertype" # Redirect to dashboard
    print("Login failed") # Debug statement
    return "Login Page"

# Recovery Page
@auth_routes.route('/recovery')
def recovery():
    print("Recovery attempt") # Debug statement
    if True: # Placeholder for actual recovery logic
        print("Recovery successful") # Debug statement
        return "Recovery Page"
    else:
        return "Recovery Failed"                
    

# Registration Page
@auth_routes.route('/register')
def register():
    print("Registration attempt") # Debug statement
    if True: # Placeholder for actual registration logic
        print("Registration successful") # Debug statement
        return "Login Page"
    else:   
        print("Registration failed") # Debug statement
        return "Registration Page"   

# Logout Route
@auth_routes.route('/logout')
def logout():
    print("Logout attempt") # Debug statement
    if True: # Placeholder for actual logout logic
        print("Logout successful") # Debug statement
    return "splash" # Redirect to splash page