from flask import Flask, session, Blueprint,render_template, request, redirect, url_for, flash
from flask_session import Session
import sqlite3

from CreateDB import DB_NAME

@login_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print("Executing:", query)
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        if user:
            session['username'] = username 
            session['email'] = email                 # Weak session state
            session['role'] = user[3]                             # Store user role in session                
            session['auth_level'] = user[0]               
            flash("Login successful", "success")
            return redirect(url_for('homepage')) 
    return render_template("Login.html")