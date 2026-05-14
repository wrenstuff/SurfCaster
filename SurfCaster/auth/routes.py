import sqlite3
import email

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

DB_NAME = "../SurfCaster.db"

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/')
def splash ():
    return "Welcome to SurfCaster! Please log in or register to continue."

# Login Page
@auth_routes.route('/login')
def login():
    return render_template('login.html')
    #print("Login attempt") # Debug statement
    #if True: # Placeholder for actual login logic
        #print("Login successful") # Debug statement
        #return "dashboard//usertype" # Redirect to dashboard
    #print("Login failed") # Debug statement
    #return "Login Page" */

@auth_routes.route('/login-form', methods=['GET','POST'])
def login_form():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        # get username and password from form
        username = request.form.get("username")
        password = request.form.get("password")

        # connect to database and check credentials
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        params = (username, password)
        print("Executing:", query)
        cursor.execute(query, params)
        user = cursor.fetchone()
        conn.close()

        # populating session with user info
        if user:
            session['username'] = user[1] 
            session['email'] = user[2]
            session['role'] = user[4]              
            flash("Login successful", "success")

            # redirect to users' dashboard based on role
            return redirect(url_for(session['role'] + '_routes.home'))
    return render_template("Login.html")

# Registration Page
@auth_routes.route('/recover')
def recover():
    return render_template('recover.html')
    #print("Registration attempt") # Debug statement
    #if True: # Placeholder for actual registration logic
        #print("Registration successful") # Debug statement
        #return "Login Page"
    #else:   
        #print("Registration failed") # Debug statement
        #return "Registration Page"   

@auth_routes.route('/signup')
def signup():
    return render_template('signup.html')
    #print("Registration attempt") # Debug statement
    #if True: # Placeholder for actual registration logic
        #print("Registration successful") # Debug statement
        #return "Login Page"
    #else:   
        #print("Registration failed") # Debug statement
        #return "Registration Page"  

@auth_routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth_routes.login'))