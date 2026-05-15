from flask import Blueprint, render_template, session, request, redirect, url_for, flash
import sqlite3
from CreateDB import DB_NAME

# blueprint creation
register_bp = Blueprint('register_bp', __name__)

#logic if we want to have it as a seperate file / calling / language
def register():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        connection.commit() 
        connection.close()
    return redirect(url_for('auth_routes.login'))
