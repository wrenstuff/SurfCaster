from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from db_models import Users
from datetime import datetime
from recover_acc import accountrecover,recovery_code, code_verifcation
from extensions import wait_time, db

hasher = PasswordHasher()
DB_NAME = "instance/SurfCaster.db"

auth_routes = Blueprint('auth_routes', __name__)

#splash 
@auth_routes.route('/')
def splash ():
    return render_template("splash.html",login_url =url_for("auth_routes.login"))
    

# Login Page
@auth_routes.route('/login', methods=["GET","POST"])
def login():
    
    if request.method == "GET":
        session.clear()
        return render_template('login.html')
    if request.method =="POST":
        # get username and password from form
        credential = request.form.get("credential").strip()
        password = request.form.get("password")
        session['logout'] = False
        #hashedpw = hasher.hash(password)
        user = Users.query.filter_by(username=credential).first() or Users.query.filter_by(email=credential).first()
        if user:
            try:
                stored_pass = user.password
                if hasher.verify(stored_pass,password):
                    # populating session with user info
                    session['user_id'] = user.id
                    session['username'] = user.username 
                    session['email'] = user.email
                    session['role'] = user.role
                    session['join_date'] = user.joindate
                    flash("Login successful", "success")
                    # redirect to users' dashboard based on role
                    wait_time()
                    return redirect(url_for(session['role'] + '_routes.home'))
                
            except VerifyMismatchError:
                flash("Invalid username or password", "error")
                return render_template("login.html")
        
        else:   
            flash("Invalid username or password", "error")
            return render_template("login.html")
        


@auth_routes.route('/signup', methods=["GET","POST"])
def signup():

    if request.method == "GET":
        return render_template("signup.html")
    
    if request.method == "POST":
        #get form data and cleanse spaces
        username = request.form.get("username").strip()
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()
        joindate = datetime.now().strftime("%Y%m%d")
        #error handling for empty fields and password length
        if not username or not email or not password:
            flash("All fields are required")
            return redirect(url_for('auth_routes.signup'))
        #error handling for password length and existing username/email
        if len(password) < 6:
            flash("Password must be at least 6 characters long")
            return redirect(url_for('auth_routes.signup'))
        #check if username or email already exists in db
        if Users.query.filter_by(username=username).first():
            flash("Username already exists")
            return redirect(url_for('auth_routes.signup'))
        #check if email already exists in db
        if Users.query.filter_by(email=email).first():
            flash("Email already exists")
            return redirect(url_for('auth_routes.signup'))
        
        #hash password and create new user
        hashedpw = hasher.hash(password)

        new_user = Users(username=username, email=email, password=hashedpw, role="user", joindate=joindate)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup successful, please log in", "success")
    return redirect(url_for('auth_routes.login'))

    

@auth_routes.route('/logout')
def logout():
    session['logout'] = True
    wait_time()
    session.clear()
    return redirect(url_for('auth_routes.login'))


#function to send recover code email
def recover_logic():
    useremail = request.form.get("user-email")
    code = recovery_code(6)

    user = Users.query.filter_by(email=useremail).first()

    if not user:
        return "user was not found"
    #temp session logic
    session["recovery_user_id"] = user.id
    session["recovery_verifcation"] = False
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
    user_id= session.get("recovery_user_id")
    if not user_id:
        return redirect(url_for('auth_routes.login'))
    if request.method == "GET":
        return render_template("recover_code.html")
    if request.method == "POST":
      input_code = request.form.get("recover-code").strip()
      correct,message  =code_verifcation(user_id,input_code)
      #correct = result[0]
      #message = result[1]

      if not correct:
          flash(message)
          return redirect(url_for("auth_routes.recover_code", error= message))
      
      if correct:
        session ["recovery_verification"] =True
        return redirect(url_for("auth_routes.reset_pw"))

@auth_routes.route('/reset_pw', methods=["GET","POST"])
def reset_pw():
    user_id= session.get("recovery_user_id")
    verification = session.get("recovery_verification")
    #user_type checks
    if not user_id or not verification:
        flash("Session expired")
        return redirect(url_for("auth_routes.login"))
    
    if request.method == "GET":
        return render_template("reset_pw.html")

  

    #get new password from form and cleanse spaces
    reset_pass = request.form.get('password', '').strip()
    password_conf = request.form.get('confirm_password', '').strip()

    #error handling
    if not reset_pass or not password_conf:
        flash("Please fill out all fields")
        return redirect(url_for("auth_routes.reset_pw"))

    if reset_pass != password_conf:
        flash("Passwords do not match")
        return redirect(url_for("auth_routes.reset_pw"))

    if len(reset_pass) < 8:
        flash("Password must be at least 8 characters long")
        return redirect(url_for("auth_routes.reset_pw"))

    # fetch user from db
    user = Users.query.filter_by(id=user_id).first()
     
    #additional check to ensure user exists before updating password
    if not user:
        flash("User not found")
        return redirect(url_for("auth_routes.recover"))

    # hash new password and update db
    user.password = hasher.hash(reset_pass)
    db.session.commit()
    # clear recovery session data
    session.clear()
    flash("Password reset successfully")
    return redirect(url_for("auth_routes.login"))

@auth_routes.route('/change_password', methods=["POST"])
def change_password():
    user_id = session.get("user_id")
    if not user_id:
        flash("Session expired")
        return redirect(url_for("auth_routes.login"))
    
    #get data from inputs
    current_password = request.form.get("current_password").strip()
    new_password = request.form.get("new_password").strip()
    confirm_password = request.form.get("confirm_password").strip()

    #error handling methods
    if not current_password or not new_password or not confirm_password:
        flash("All fields are required")
        return redirect(url_for( session.get('role') + "_routes.settings"))
    
    if len(new_password) < 6:
        flash("New password must be at least 6 characters long")
        return redirect(url_for( session.get('role') + "_routes.settings"))
    
    if new_password != confirm_password:
        flash("New password and confirmation do not match")
        return redirect(url_for( session.get('role') + "_routes.settings"))

    #get user info from db
    user = Users.query.filter_by(id=user_id).first()
    if not user:
        flash("User not found")
        return redirect(url_for("auth_routes.login"))
    
    #check current password and update to new password if correct
    try:
        if hasher.verify(user.password, current_password):
            #update to new password
            user.password = hasher.hash(new_password)
            db.session.commit()
            flash("Password changed successfully", "success")
            return redirect(url_for(session.get('role') + "_routes.settings"))
        else:
            flash("Current password is incorrect")
            return redirect(url_for(session.get('role') + "_routes.settings"))
    except VerifyMismatchError:
        flash("Current password is incorrect")
        return redirect(url_for(session.get('role') + "_routes.settings"))
    
@auth_routes.route('/delete_account', methods=["POST"])
def delete_account():
    print("DELETE ROUTE HIT")
    #gets user id from session
    user_id = session.get("user_id")
    #fetch user from db
    user = Users.query.filter_by(id=user_id).first()
    if not user:
        flash("session has expired")
        return redirect(url_for("auth_routes.login"))
    if user:
        #delete user from db
        db.session.delete(user)
        db.session.commit()
    #clear session
    session.clear()
    flash("Account deleted successfully")
    return redirect(url_for("auth_routes.login"))