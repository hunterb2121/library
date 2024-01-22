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
    
    shelves = db_cur.execute("SELECT number FROM bookshelf WHERE user_id = ?", (session["user_id"],))
    shelves = shelves.fetchall()
    print(shelves)

    library = dict()
    for shelf in shelves:
        print(shelf)
        books = db_cur.execute("SELECT books_shelf.id, books_shelf.bookshelf_id, books_shelf.books_id, books_shelf.user_id, books.book_name, books.author, books.cover_color, books.publishing_house, books.fiction_nonfiction, books.genre, books.been_read, books.ISBN FROM books_shelf INNER JOIN books ON books_shelf.books_id = books.id WHERE books_shelf.bookshelf_id = ?", (shelf[0],))
        books = books.fetchall()
        print(books)

        if len(books) != 0:
            for book in books:
                print(book)
                if book[8] == 0:
                    fiction_nonfiction = "Non-Fiction"
                elif book[8] == 1:
                    fiction_nonfiction = "Fiction"

                if book[10] == 0:
                    read = "Not Read"
                elif book[10] == 1:
                    read = "Read"

                if shelf[0] in library:
                    print(library[shelf[0]])
                    library[shelf[0]].append({"id": book[2], "title": book[4], "author": book[5], "color": book[6], "publisher": book[7], "fiction_nonfiction": fiction_nonfiction, "genre": book[9], "read": read, "isbn": book[11]})
                else:
                    library[shelf[0]] = [{"id": book[2], "title": book[4], "author": book[5], "color": book[6], "publisher": book[7], "fiction_nonfiction": fiction_nonfiction, "genre": book[9], "read": read, "isbn": book[11]}]

        else:
            library[shelf[0]] = [{"id": None, "title": None, "author": None, "color": None, "publisher": None, "fiction_nonfiction": None, "genre": None, "read": None, "isbn": None}]

    print(library)

    db_cur.close()

    session["edit_book_num"] = request.args.get("edit_book")
    session["remove_book_num"] = request.args.get("remove_book")
    session["edit_shelf_num"] = request.args.get("edit_shelf")
    session["remove_shelf_num"] = request.args.get("remove_shelf")

    return render_template("index.html", library=library)


@app.route("/add_book", methods=["GET", "POST"])
@login_required
def add_book():
    if request.method == "POST":
        ...

    else:
        return render_template("add_book.html")


@app.route("/remove_book", methods=["GET", "POST"])
@login_required
def remove_book():
    ...


@app.route("/edit_book", methods=["GET", "POST"])
@login_required
def edit_book():
    if request.method == "POST":
        ...

    else:
        return render_template("edit_book.html")


@app.route("/add_shelf", methods=["GET", "POST"])
@login_required
def add_shelf():
    if request.method == "POST":
        try:
            db_con, db_cur = get_db_connection()
        except sqlite3.OperationalError:
            return error("Error connecting to database. Try again later.")
        
        if not request.form.get("shelf_number"):
            db_cur.close()
            return error("Must choose a shelf number")
        
        db_cur.execute("INSERT INTO bookshelf (number, user_id) VALUES (?, ?)", (request.form.get("shelf_number"), session["user_id"],))
        db_con.commit()
        db_cur.close()

        return redirect("/")
    
    else:
        return render_template("add_shelf.html")


@app.route("/remove_shelf", methods=["GET", "POST"])
@login_required
def remove_shelf():
    ...


@app.route("/edit_shelf", methods=["GET", "POST"])
@login_required
def edit_shelf():
    if request.method == "POST":
        try:
            db_con, db_cur = get_db_connection()
        except sqlite3.OperationalError:
            return error("Error connecting to database. Try again later.")
        
        if not request.form.get("shelf_number"):
            db_cur.close()
            return error("Must choose a new shelf number")
        
        db_cur.execute("UPDATE bookshelf SET number = ? WHERE id = ? AND user_id = ?", (request.form.get("shelf_number"), session["current_shelf_num"], session["user_id"],))
        db_con.commit()
        db_cur.close()

        return redirect("/")

    else:
        return render_template("edit_shelf.html", current_shelf_num=session["edit_shelf_num"])


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
        print(usernames)
        if usernames:
            db_cur.close()
            return error("Username already exists")
        
        emails = db_cur.execute("SELECT email FROM users")
        emails = emails.fetchall()
        print(emails)
        if emails:
            db_cur.close()
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
            db_cur.close()
            error("User does not exist")

        # Check if password matches for the username
        if not check_password_hash(db_cur.execute("SELECT hash FROM users WHERE username = ? or email = ?", (request.form.get("username_email"), request.form.get("username_email"),)).fetchone()[0], request.form.get("password")):
            db_cur.close()
            error("Password could not be verified")

        session["user_id"] = get_session_user(request.form.get("username_email"))

        db_cur.close()

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    session.clear()

    return redirect("/")

"""
@app.route("/account")
@login_required
def account():
    ...


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