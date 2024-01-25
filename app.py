import sqlite3

from database import execute_query, fetch_all, fetch_one
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required, get_session_user, error
from library_objects import Shelf, Book, User, Library


app = Flask(__name__)
app.config.from_pyfile("config.py")
Session(app)


@app.route("/")
@login_required
def index():
    user_library = Library()
    user_shelves = Shelf.get_shelf_by_user(session["user_id"])
    user_books = Book.get_books_by_user(session["user_id"])

    for shelf in user_shelves:
        user_library.add_shelf_to_library(shelf)
    for book in user_books:
        user_library.add_book_to_library(book)

    # Show all books that are on each shelf and display in index.html with a dictionary called library
    # library = {shelf_number: {book_id, title, author, color, publisher, fiction_nonfiction, genre, read, isbn}}
    book_shelves = dict()
    for book in user_library.get_books_in_library():
        book_id = book[0]
        shelf_id = user_library.get_shelf_for_book(book_id, 1)[0]
        if book[7] == 0:
            fiction_nonfiction = "nonfiction"
        elif book[7] == 1:
            fiction_nonfiction = "fiction"
        if book[9] == 0:
            read = "Not Read"
        elif book[9] == 1:
            read = "Read"
        if shelf_id in book_shelves:
            book_shelves[shelf_id].append({"title": book[1], "author": book[2], "pages": book[3], "color": book[4], "publisher": book[5], "published_date": book[6], "fiction_nonfiction": fiction_nonfiction, "genre": book[8], "read": read, "isbn": book[10], "added_date": book[11]})
        else:
            book_shelves[shelf_id] = [{"title": book[1], "author": book[2], "pages": book[3], "color": book[4], "publisher": book[5], "published_date": book[6], "fiction_nonfiction": fiction_nonfiction, "genre": book[8], "read": read, "isbn": book[10], "added_date": book[11]}]
    return render_template("index.html", library=book_shelves)


@app.route("/add_book", methods=["POST"])
@login_required
def add_book():
    return redirect("/")


@app.route("/remove_book", methods=["POST"])
@login_required
def remove_book():
    return redirect("/")


@app.route("/edit_book", methods=["POST"])
@login_required
def edit_book():
    return redirect("/")


@app.route("/add_shelf", methods=["POST"])
@login_required
def add_shelf():
    return redirect("/")


@app.route("/remove_shelf", methods=["POST"])
@login_required
def remove_shelf():
    return redirect("/")


@app.route("/edit_shelf", methods=["POST"])
@login_required
def edit_shelf():
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    # Check if request is POST
    if request.method == "POST":
        # Check if form is filled out before submitting
        if not request.form.get("username"):
            return error("Please enter an username")
        if not request.form.get("email"):
            return error("Please enter an email")
        if not request.form.get("password"):
            return error("Please enter a password")
        if not request.form.get("verify"):
            return error("Please verify password")
        
        # Validate email and password meet requirments
        if not User.validate_email(request.form.get("email")):
            return error("Email not valid")
        if not User.validate_password(request.form.get("password")):
            return error("Please make the password more complex")
        
        # Verify passwords match
        hash = User.get_hash(request.form.get("password"))
        if not User.compare_passwords(hash, request.form.get("verify")):
            return error("Passwords do not match")

        # Check if username and/or email already exist
        if User.get_user_by_username(request.form.get("username")) is not None:
            return error("Username already exists")
        if User.get_user_by_email(request.form.get("email")) is not None:
            return error("Email already exists")
        
        # Add user to the database
        User.add_user(request.form.get("username"), request.form.get("email"), hash, datetime.utcnow())

        # Assign user_id to session variable
        session["user_id"] = get_session_user(request.form.get("username"))

        return redirect("/")

    # Check if request is GET
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check for username and password fields being filled out
        if not request.form.get("username_email"):
            error("Please enter username or email")
        if not request.form.get("password"):
            return error("Error connecting to database. Try again later.")
        
        # Check if username or email matches entry in database
        if not User.get_user_by_username(request.form.get("username_email")):
            return error("User does not exist")
        
        session["user_id"] = get_session_user(request.form.get("username_email"))

        # Check if password matches
        hash = User.get_user_hash_by_id(session["user_id"])
        if not User.compare_passwords(hash, request.form.get("password")):
            session.clear()
            return error("Password does not match password on file")
        
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    session.clear()

    return redirect("/")


@app.route("/account")
@login_required
def account():
    return render_template("account.html")


@app.route("/edit_username", methods=["GET", "POST"])
@login_required
def edit_username():
    ...


@app.route("/edit_email", methods=["GET", "POST"])
@login_required
def edit_email():
    ...


@app.route("/edit_password", methods=["GET", "POST"])
@login_required
def edit_password():
    ...
