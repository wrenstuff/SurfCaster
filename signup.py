from flask import Blueprint, render_template, session, request, redirect, url_for, flash
import sqlite3
from CreateDB import DB_NAME

# blueprint creation
register_bp = Blueprint('register_bp', __name__)

def register():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")  
        role = 'user'  
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        query = f"INSERT INTO users (username, email, password, role) VALUES ('{username}', '{email}', '{password}', '{role}')"
        print("Executing:", query)
        cursor.execute(query)
        conn.commit()
        conn.close()
        flash("Registration successful", "success")
        return redirect(url_for('login')) 
    return render_template("Register.html")
