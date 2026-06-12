import sqlite3
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from db_models import Users
from datetime import datetime ,timedelta, timezone
from recover_acc import accountrecover,recovery_code
import time

hasher = PasswordHasher()
DB_NAME = "instance/SurfCaster.db"

auth_routes = Blueprint('auth_routes', __name__)

#splash 
@auth_routes.route('/')
def splash ():
    return render_template("splash.html")
    

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

        session['logout'] = False
        #hashedpw = hasher.hash(password)
        user = Users.query.filter_by(username=username).first()
        if user:
            try:
                stored_pass = user.password
                if hasher.verify(stored_pass,password):
                    # populating session with user info
                    session['user_id'] = user.id
                    session['username'] = user.username 
                    session['email'] = user.email
                    session['role'] = user.role            
                    flash("Login successful", "success")
                    # redirect to users' dashboard based on role
                    time.sleep(1.5)
                    return redirect(url_for(session['role'] + '_routes.home'))
                
            except VerifyMismatchError:
                flash("Invalid username or password", "error")
                return render_template("login.html")
        
        else:   
            flash("Invalid username or password", "error")
            return render_template("login.html")
#function to send recover code email
def recover_logic():
    useremail = request.form.get("user-email")
    code = recovery_code(6)
    accountrecover(useremail,code)

# Recover page
@auth_routes.route('/recover' , methods=["GET","POST"])
def recover():
    if request.method == "GET":
        return render_template("recover.html")
    if request.method == "POST":
        recover_logic()
        return redirect(url_for("auth_routes.recover_code"))

#code input
@auth_routes.route('/recover_code' , methods=["GET","POST"])
def recover_code():
    if request.method == "GET":
        return render_template("recover_code.html")
    if request.method == "POST":
        
        return render_template('recover_code.html')

@auth_routes.route('/resend_recovery_code', methods =["POST"] )
def resend():
    recover_logic()

    



@auth_routes.route('/signup', methods=["GET","POST"])
def signup():

    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        connection = sqlite3.connect(DB_NAME)
        joindate = datetime.now().strftime("%Y%m%d")
        cursor = connection.cursor()
        hashedpw = hasher.hash(password)
        cursor.execute("INSERT INTO users (username, email, password, role, joindate) VALUES (?, ?, ?, ?, ?)", (username, email, hashedpw, "user", joindate))
        connection.commit() 
        connection.close()
    return redirect(url_for('auth_routes.login'))

    

@auth_routes.route('/logout')
def logout():
    session['logout'] = True
    time.sleep(1.5)
    session.clear()
    return redirect(url_for('auth_routes.login'))