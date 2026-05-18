import sqlite3
import email
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from argon2 import PasswordHasher
from user_model import Users

hasher = PasswordHasher()
DB_NAME = "instance/SurfCaster.db"

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/')
def splash ():
    return "Welcome to SurfCaster! Please log in or register to continue."

# Login Page
@auth_routes.route('/login', methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    if request.method =="POST":
        conn = sqlite3.connect(DB_NAME)
        # get username and password from form
        username = request.form.get("username")
        password = request.form.get("password")

        #hashedpw = hasher.hash(password)
        user = Users.query.filter_by(username=username).first()
        stored_pass = user.password
        if hasher.verify(stored_pass,password):
        # populating session with user info
            session['username'] = user.username 
            session['email'] = user.email
            session['role'] = user.role            
            flash("Login successful", "success")

            # redirect to users' dashboard based on role
            return redirect(url_for(session['role'] + '_routes.home'))
    return render_template("login.html")

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

@auth_routes.route('/signup', methods=["GET","POST"])
def signup():

    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        hashedpw = hasher.hash(password)
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashedpw))
        connection.commit() 
        connection.close()
    return redirect(url_for('auth_routes.login'))

    

@auth_routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth_routes.login'))