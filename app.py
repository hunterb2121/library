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

    return render_template("index.html", library=library)


@app.route("/add_book", methods=["POST"])
@login_required
def add_book():
    if not request.form.get("book_title"):
        return error("Need to enter book title")
    if not request.form.get("book_author"):
        return error("Need to enter author")
    if not request.form.get("color"):
        return error("Need to enter book color")
    if not request.form.get("publisher"):
        return error("Need to enter publishing house")
    if not request.form.get("fiction_nonfiction"):
        return error("Need to enter whether book is fiction or non-fiction")
    if not request.form.get("genre"):
        return error("Need to enter book genre")
    if not request.form.get("read_not_read"):
        return error("Need to enter if book has been read or not")
    if not request.form.get("isbn"):
        return error("Need to enter ISBN")
    
    fiction_nonfiction = request.form.get("fiction_nonfiction")
    if fiction_nonfiction == "fiction":
        fiction_nonfiction = 1
    elif fiction_nonfiction == "nonfiction":
        fiction_nonfiction = 0

    been_read = request.form.get("read_not_read")
    if been_read == "read":
        been_read = 1
    elif been_read == "not_read":
        been_read = 0
    
    try:
        db_con, db_cur = get_db_connection()
    except sqlite3.OperationalError:
        return error("Error connecting to database. Try again later.")

    db_cur.execute("INSERT INTO books (book_name, author, cover_color, publishing_house, fiction_nonfiction, genre, been_read, ISBN, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (request.form.get("book_title"), request.form.get("book_author"), request.form.get("color"), request.form.get("publisher"), fiction_nonfiction, request.form.get("genre"), been_read, request.form.get("isbn"), session["user_id"],))
    db_con.commit()
    book_id = db_cur.execute("SELECT id FROM books WHERE book_name = ? AND user_id = ?", (request.form.get("book_title"), session["user_id"],))
    book_id = book_id.fetchone()[0]
    print(book_id)
    bookshelf_id = db_cur.execute("SELECT id FROM bookshelf WHERE number = ? AND user_id = ?", (request.form.get("shelf_number"), session["user_id"],))
    bookshelf_id = bookshelf_id.fetchone()[0]
    print(bookshelf_id)
    db_cur.execute("INSERT INTO books_shelf (bookshelf_id, books_id, user_id) VALUES (?, ?, ?)", (bookshelf_id, book_id, session["user_id"],))
    books_shelf = db_cur.execute("SELECT id FROM books_shelf WHERE bookshelf_id = ? AND books_id = ? AND user_id = ?", (bookshelf_id, book_id, 1))
    books_shelf = books_shelf.fetchone()[0]
    print(books_shelf)
    db_con.commit()
    db_cur.close()

    return redirect("/")


@app.route("/remove_book", methods=["POST"])
@login_required
def remove_book():
    try:
        db_con, db_cur = get_db_connection()
    except sqlite3.OperationalError:
        return error("Error connecting to database. Try again later.")
    
    db_cur.execute("DELETE FROM books WHERE id = ? AND user_id = ?", (request.form.get("remove_book"), session["user_id"],))
    db_con.commit()
    db_cur.close()

    return redirect("/")


@app.route("/edit_book", methods=["POST"])
@login_required
def edit_book():
    try:
        db_con, db_cur = get_db_connection()
    except sqlite3.OperationalError:
        return error("Error connecting to database. Try again later.")
    
    if request.form.get("book_title"):
        db_cur.execute("UPDATE books SET book_name = ? WHERE id = ? AND user_id = ?", (request.form.get("book_title"), request.form.get("book_id"), session["user_id"],))
        db_con.commit()
    if request.form.get("book_author"):
        db_cur.execute("UPDATE books SET author = ? WHERE id = ? AND user_id = ?", (request.form.get("book_author"), request.form.get("book_id"), session["user_id"],))
        db_con.commit()
    if request.form.get("color"):
        db_cur.execute("UPDATE books SET cover_color = ? WHERE id = ? AND user_id = ?", (request.form.get("color"), request.form.get("book_id"), session["user_id"],))
        db_con.commit()
    if request.form.get("publisher"):
        db_cur.execute("UPDATE books SET publishing_house = ? WHERE id = ? AND user_id = ?", (request.form.get("publisher"), request.form.get("book_id"), session["user_id"],))
        db_con.commit()
    if request.form.get("fiction_nonfiction"):
        if request.form.get("fiction_nonfiction") == "fiction":
            fiction_nonfiction = 1
        elif request.form.get("fiction_nonfiction") == "nonfiction":
            fiction_nonfiction = 0
        db_cur.execute("UPDATE books SET fiction_nonfiction = ? WHERE id = ? AND user_id = ?", (fiction_nonfiction, request.form.get("book_id"), session["user_id"],))
        db_con.commit()
    if request.form.get("genre"):
        db_cur.execute("UPDATE books SET genre = ? WHERE id = ? AND user_id = ?", (request.form.get("genre"), request.form.get("book_id"), session["user_id"],))
        db_con.commit()
    if request.form.get("read_not_read"):
        if request.form.get("read_not_read") == "read":
            read_not_read = 1
        elif request.form.get("read_not_read") == "not_read":
            read_not_read = 0
        db_cur.execute("UPDATE books SET been_read = ? WHERE id = ? AND user_id = ?", (read_not_read, request.form.get("book_id"), session["user_id"],))
        db_con.commit()
    if request.form.get("book_isbn"):
        db_cur.execute("UPDATE books SET ISBN = ? WHERE id = ? AND user_id = ?", (request.form.get("isbn"), request.form.get("book_id"), session["user_id"],))
        db_con.commit()

    db_cur.close()

    return redirect("/")


@app.route("/add_shelf", methods=["POST"])
@login_required
def add_shelf():
    if not request.form.get("shelf_number"):
        return error("Need to enter new shelf number")
    
    try:
        db_con, db_cur = get_db_connection()
    except sqlite3.OperationalError:
        return error("Error connecting to database. Try again later.")
    
    db_cur.execute("INSERT INTO bookshelf (number, user_id) VALUES (?, ?)", (request.form.get("shelf_number"), session["user_id"],))
    db_con.commit()
    db_cur.close()

    return redirect("/")


@app.route("/remove_shelf", methods=["POST"])
@login_required
def remove_shelf():
    try:
        db_con, db_cur = get_db_connection()
    except sqlite3.OperationalError:
        return error("Error connecting to database. Try again later.")
    
    db_cur.execute("DELETE FROM bookshelf WHERE number = ? AND user_id = ?", (request.form.get("remove_shelf_id"), session["user_id"],))
    db_con.commit()
    db_cur.close()

    return redirect("/")


@app.route("/edit_shelf", methods=["POST"])
@login_required
def edit_shelf():
    try:
        db_con, db_cur = get_db_connection()
    except sqlite3.OperationalError:
        return error("Error connecting to database. Try again later.")
    
    if not request.form.get("shelf_number"):
        db_cur.close()
        return error("Must choose a new shelf number")
    
    bookshelf_nums = db_cur.execute("SELECT number FROM bookshelf WHERE user_id = ?", (session["user_id"],))
    bookshelf_nums = bookshelf_nums.fetchall()
    existing_shelves = list()
    if bookshelf_nums is not None:
        for nums in bookshelf_nums:
            existing_shelves.append(nums[0])
        
    if request.form.get("shelf_number") in existing_shelves:
        db_cur.close()
        return error("Shelf number already exists")
    
    db_cur.execute("UPDATE bookshelf SET number = ? WHERE id = ? AND user_id = ?", (request.form.get("shelf_number"), request.form.get("current_shelf_number"), session["user_id"],))
    db_con.commit()
    db_cur.close()

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