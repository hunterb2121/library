import sqlite3

from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required, get_db_connection, get_session_user, error
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config.from_pyfile("config.py")
Session(app)


@app.route("/")
@login_required
def index():
    try:
        db_cur = get_db_connection()[1]
    except sqlite3.OperationalError:
        return error("Error connecting to database. Try again later.")
    
    data = db_cur.execute("SELECT books_shelf.id, books_shelf.user_id, bookshelf.number, books.book_name, books.author, books.cover_color, books.publishing_house, books.fiction_nonfiction, books.genre, books.been_read, books.ISBN FROM books_shelf INNER JOIN bookshelf ON books_shelf.bookshelf_id = bookshelf.id INNER JOIN books ON books_shelf.books_id = books.id WHERE books_shelf.user_id = ?", (session["user_id"],))
    data = data.fetchall()
    print(data)

    library = dict()
    for item in data:
        if item[7] == 0:
            fiction_nonfiction = "Non-fiction"
        elif item[7] == 1:
            fiction_nonfiction = "Fiction"

        if item[9] == 0:
            read = "Not read"
        elif item[9] == 1:
            read = "Read"

        if item[2] in library:
            library[item[2]].append({"title": item[3], "author": item[4], "color": item[5], "publisher": item[6], "fiction_nonfiction": fiction_nonfiction, "genre": item[8], "read": read, "isbn": item[10]})

        else:
            library[item[2]] = [{"title": item[3], "author": item[4], "color": item[5], "publisher": item[6], "fiction_nonfiction": fiction_nonfiction, "genre": item[8], "read": read, "isbn": item[10]}]

    print(library)

    return render_template("index.html", library=library)


@app.route("/add_book", methods=["GET", "POST"])
@login_required
def add_book():
    ...


@app.route("/remove_book", methods=["GET", "POST"])
@login_required
def remove_book():
    ...


@app.route("/edit_book", methods=["GET", "POST"])
@login_required
def edit_book():
    ...


@app.route("/add_shelf", methods=["GET", "POST"])
@login_required
def add_shelf():
    ...


@app.route("/remove_shelf", methods=["GET", "POST"])
@login_required
def remove_shelf():
    ...


@app.route("/edit_shelf", methods=["GET", "POST"])
@login_required
def edit_shelf():
    ...


@app.route("/add_book_shelf", methods=["GET", "POST"])
@login_required
def add_book_shelf():
    ...


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

        # Check if password matches verifications
        hash = generate_password_hash(request.form.get("password"))
        if not check_password_hash(hash, request.form.get("verify")):
            return error("Passwords must match")

        # Open database connection
        try: 
            db_con, db_cur = get_db_connection()
        except sqlite3.OperationalError:
            return error("Error connecting to database. Try again later.")
        
        # Check if username and/or email exists
        usernames = db_cur.execute("SELECT username FROM users")
        usernames = usernames.fetchall()
        if request.form.get("username") in usernames:
            return error("Username already exists")
        
        emails = db_cur.execute("SELECT email FROM users")
        emails = emails.fetchall()
        if request.form.get("email") in emails:
            return error("Email already exists")

        # Create user account in database
        db_cur.execute("INSERT INTO users (username, email, hash, created_date) VALUES (?, ?, ?, ?)", (request.form.get("username"), request.form.get("email"), hash, datetime.utcnow(),))
        db_con.commit()
        db_cur.close()

        # Assign user to session
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

        try:
            db_cur = get_db_connection()[1]
        except sqlite3.OperationalError:
            return error()

        # Check if username exists
        if not db_cur.execute("SELECT id FROM users WHERE username = ? or email = ?", (request.form.get("username_email"), request.form.get("username_email"),)):
            error("User does not exist")

        # Check if password matches for the username
        if not check_password_hash(db_cur.execute("SELECT hash FROM users WHERE username = ? or email = ?", (request.form.get("username_email"), request.form.get("username_email"),))):
            error("Password could not be verified")

        session["user_id"] = get_session_user(request.form.get("username_email"))

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    session.clear()

    return redirect("/")

"""
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
"""