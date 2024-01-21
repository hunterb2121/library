from flask import redirect, render_template, session
from functools import wraps
import sqlite3


# Function to make login required for users to see certain routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Function to return an error message
def error(message, code=400):
    return render_template("error.html", message=message, code=code)


# Function to connect to the database and get the connection and cursor
def get_db_connection():
    db_con = sqlite3.connect("users.db")
    db_cur = db_con.cursor()
    return db_con, db_cur


# Function to get the user id of the current user
def get_session_user(username):
    try:
        db_cur = get_db_connection()[1]
        user_id = db_cur.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, username,))
        user_id = user_id.fetchone()
        if user_id == None:
            return error("User does not exist")
        user_id = user_id[0]
        db_cur.close()
        return user_id
    except sqlite3.OperationalError:
        return error("Error connecting to database. Please try again later.")
