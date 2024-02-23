import requests

from database import fetch_one
from flask import redirect, render_template, session
from functools import wraps


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


# Function to get the user id of the current user
def get_session_user(username):
    user_id = fetch_one("SELECT id FROM users WHERE username = ? OR email = ?", (username, username,))
    if user_id == None:
        return error("User does not exist")
    user_id = user_id[0]
    return user_id


# Function to get the book info from the Google Books API using the ISBN of the book
def get_book_info(isbn):
    key = "AIzaSyBoPGcCG_hpd-h4b0r0iksVwKDHyQTUcAc"
    api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={key}"

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        book_info = data["items"][0]["volumeInfo"]

        return book_info
    
    else:
        return {"error": "Failed to retrieve book information", "code": response.status_code}

