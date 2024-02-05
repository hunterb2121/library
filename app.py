import logging

from datetime import datetime
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required, get_session_user, error
from library_objects import Shelf, Book, User, Library


# Implement search functionality to search for books based on title, author, genre, cover color
# Need to get all books based on those parameters and have it display the title, shelf, and if hovered over the rest of the book's info


logging.basicConfig(filename='app.log', encoding="utf-8", level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s : %(message)s")
app = Flask(__name__)
app.config.from_pyfile("config.py")
Session(app)

app.logger.setLevel(logging.DEBUG)


@app.route("/")
@login_required
def index():
    user_library = Library()
    logging.info(f"User Library : {user_library}")
    user_shelves = Shelf.get_shelf_by_user(session["user_id"])
    logging.info(f"User Shelves : {user_shelves}")
    user_books = Book.get_books_by_user(session["user_id"])
    logging.info(f"User Books : {user_books}")

    book_shelves = dict()
    logging.info(f"Book Shelves : {book_shelves}")
    if user_shelves is not None:
        logging.info("User Shevles is not None")
        for shelf in user_shelves:
            logging.info(f"Shelf : {shelf}")
            user_library.add_shelf_to_library(shelf)
        logging.info(f"User Library : {user_library}")

    if user_books is not None:
        logging.info("User Books is not None")
        for book in user_books:
            logging.info(f"Book : {book}")
            user_library.add_book_to_library(book)
        logging.info(f"User Library : {user_library}")

    # Show all books that are on each shelf and display in index.html with a dictionary called library
    # library = {shelf_number: {book_id, title, author, color, publisher, fiction_nonfiction, genre, read, isbn}}
    for book in user_library.get_books_in_library():
        book_id = book[0]
        logging.info(f"Book ID : {book_id}")
        shelf_id = user_library.get_shelf_for_book(book_id, session["user_id"])
        logging.info(f"Shelf ID : {shelf_id}")
        if shelf_id is None:
            logging.info(f"Shelf ID is NONE : Deleting Books on Shelf")
            Book.delete_book_by_id(book_id, session["user_id"])
            continue
        shelf_num = Shelf.get_shelf_number(shelf_id[0], session["user_id"])
        logging.info(f"Shelf Number : {shelf_num}")
        if shelf_num is None:
            logging.info(f"Shelf Num is NONE : Deleting Books on Shelf")
            Book.delete_book_by_id(shelf_id, session["user_id"])
            continue
        shelf_num = shelf_num[0]
        logging.info(f"Shelf Num : {shelf_num}")
        fiction_nonfiction = ""
        read = ""
        if book[8] == 0:
            fiction_nonfiction = "nonfiction"
        elif book[8] == 1:
            fiction_nonfiction = "fiction"
        if book[10] == 0:
            read = "Not Read"
        elif book[10] == 1:
            read = "Read"
        if shelf_num in book_shelves:
            logging.info(f"Shelf Num : {shelf_num} : in book_shelves : {book_shelves}")
            book_shelves[shelf_num].append({"book_id": book[0], "title": book[1], "author": book[2], "pages": book[3], "color": book[4], "color_name": book[5], "publisher": book[6], "published_date": book[7], "fiction_nonfiction": fiction_nonfiction, "genre": book[9], "read": read, "isbn": book[11], "added_date": book[12]})
            logging.info(f"Successfully Added Book to Shelf : {book_shelves}")
        else:
            logging.info(f"Shelf Num : {shelf_num} : not in book_shelves : {book_shelves}")
            book_shelves[shelf_num] = [{"book_id": book[0], "title": book[1], "author": book[2], "pages": book[3], "color": book[4], "color_name": book[5], "publisher": book[6], "published_date": book[7], "fiction_nonfiction": fiction_nonfiction, "genre": book[9], "read": read, "isbn": book[11], "added_date": book[12]}]
            logging.info(f"Successfully Created Shelf and Added Book to Shelf : {book_shelves}")
    for shelf in user_library.get_shelves_in_library():
        shelf_num = Shelf.get_shelf_number(shelf[0], session["user_id"])[0]
        logging.info(f"Shelf Number : {shelf_num}")
        if shelf_num not in book_shelves:
            logging.info(f"Shelf Num : {shelf_num} : not in book_shelves")
            book_shelves[shelf_num] = []

    logging.info(f"Final Book Shelves : {book_shelves}")
    book_shelves = dict(sorted(book_shelves.items()))
    logging.info(f"Sorted Book Shelves : {book_shelves}")
    return render_template("index.html", library=book_shelves)


@app.route("/add_book", methods=["POST"])
@login_required
def add_book():
    logging.info("==============================/nAdding Book/n==============================")
    if not request.form.get("book_title"):
        logging.error(f"Error : Book Title Not Entered")
        return error("Please add book's title")
    if not request.form.get("book_author"):
        logging.error(f"Error : Book Author Not Entered")
        return error("Please add book's author")
    if not request.form.get("pages"):
        logging.error(f"Error : Book Pages Not Entered")
        return error("Please add number of book's pages")
    if not request.form.get("color"):
        logging.error(f"Error : Book Cover Color Not Entered")
        return error("Please add book's cover color")
    if not request.form.get("publisher"):
        logging.error(f"Error : Book Publisher Not Entered")
        return error("Please add book's publisher")
    if not request.form.get("published_date"):
        logging.error(f"Error : Book Published Date Not Entered")
        return error("Please add book's published date")
    if not request.form.get("fiction_nonfiction"):
        logging.error(f"Error : Book Fiction or Nonfiction Not Entered")
        return error("Please add whether book is fiction or nonfiction")
    if not request.form.get("genre"):
        logging.error(f"Error : Book Genre Not Entered")
        return error("Please add book's genre")
    if not request.form.get("read_not_read"):
        logging.error(f"Error : Book Read or Not Read Not Entered")
        return error("Please add whether you have read the book or not")
    if not request.form.get("isbn"):
        logging.error(f"Error : Book ISBN Not Entered")
        return error("Please add book's ISBN")
    
    added_date = datetime.utcnow()
    logging.info(f"Current DateTime : {added_date}")
    logging.info(f"Adding Book from Form")
    Book.add_book(request.form.get("book_title"), request.form.get("book_author"), request.form.get("pages"), request.form.get("color"), request.form.get("publisher"), request.form.get("published_date"), request.form.get("fiction_nonfiction"), request.form.get("genre"), request.form.get("read_not_read"), request.form.get("isbn"), added_date, session["user_id"])

    Shelf.add_book_to_shelf_by_num(request.form.get("shelf_number"), Book.get_book_id_by_title_added_date(request.form.get("book_title"), added_date, session["user_id"])[0], session["user_id"])

    return redirect("/")


@app.route("/remove_book", methods=["POST"])
@login_required
def remove_book():
    logging.info("==============================/nRemoving Book/n==============================")
    logging.info(f"Hidden Book ID {request.form.get('book_id')}")
    Book.delete_book_by_id(request.form.get("book_id"), session["user_id"])
    return redirect("/")


@app.route("/edit_book", methods=["POST"])
@login_required
def edit_book():
    logging.info("==============================/nEditing Book/n==============================")
    logging.info(f"Hidden Book ID {request.form.get('book_id')}")
    if request.form.get("book_title"):
        logging.info("Editing Book Title")
        Book.edit_book(request.form.get("book_id"), "title", request.form.get("book_title"), session["user_id"])
    if request.form.get("book_author"):
        logging.info("Editing Book Author")
        Book.edit_book(request.form.get("book_id"), "author", request.form.get("book_author"), session["user_id"])
    if request.form.get("pages"):
        logging.info("Editing Book Pages")
        Book.edit_book(request.form.get("book_id"), "pages", request.form.get("pages"), session["user_id"])
    if request.form.get("color"):
        logging.info("Editing Book Cover Color")
        Book.edit_book(request.form.get("book_id"), "cover_color", request.form.get("color"), session["user_id"])
    if request.form.get("publisher"):
        logging.info("Editing Book Publisher")
        Book.edit_book(request.form.get("book_id"), "publishing_house", request.form.get("publisher"), session["user_id"])
    if request.form.get("published_date"):
        logging.info("Editing Book Published Date")
        Book.edit_book(request.form.get("book_id"), "published_date", request.form.get("published_date"), session["user_id"])
    if request.form.get("fiction_nonfiction"):
        logging.info("Editing Book Fiction or Nonfiction")
        Book.edit_book(request.form.get("book_id"), "fiction_nonfiction", request.form.get("fiction_nonfiction"), session["user_id"])
    if request.form.get("genre"):
        logging.info("Editing Book Genre")
        Book.edit_book(request.form.get("genre"), "title", request.form.get("genre"), session["user_id"])
    if request.form.get("read"):
        logging.info("Editing Book Read or Not Read")
        Book.edit_book(request.form.get("book_id"), "been_read", request.form.get("read"), session["user_id"])
    if request.form.get("isbn"):
        logging.info("Editing Book ISBN")
        Book.edit_book(request.form.get("book_id"), "ISBN", request.form.get("isbn"), session["user_id"])
    return redirect("/")


@app.route("/search")
@login_required
def search():
    logging.info("==============================/nSearching Book/n==============================")
    if not request.form.get("search_bar"):
        logging.error("Nothing searched")
        return redirect("/")
    
    library = dict()

    if request.form.get("search_by") == "title":
        logging.info(f"Searching books by TITLE {request.form.get('search_bar')}")
        results = Book.search_books_by_title(request.form.get("search_bar"), session["user_id"])

        for book in results:
            if book[8] == 0:
                fiction_nonfiction = "Nonfiction"
            if book[8] == 1:
                fiction_nonfiction = "Fiction"
            if book[10] == 0:
                read = "Not Read"
            if book[10] == 1:
                read = "Read"
            
            shelf_id = Library.get_shelf_for_book(book[0], session["user_id"])[0]
            if book[0] not in library:
                library[book[0]] = {"title": book[1], "author": book[2], "pages": book[3], "color": book[4], "color_name": book[5], "publisher": book[6], "published_date": book[7], "fiction_nonfiction": fiction_nonfiction, "genre": book[9], "read": read, "isbn": book[11], "shelf_id": shelf_id}

    elif request.form.get("search_by") == "author":
        logging.info(f"Searching books by AUTHOR {request.form.get('search_bar')}")
        results = Book.search_books_by_author(request.form.get("search_bar"), session["user_id"])

        for book in results:
            if book[8] == 0:
                fiction_nonfiction = "Nonfiction"
            if book[8] == 1:
                fiction_nonfiction = "Fiction"
            if book[10] == 0:
                read = "Not Read"
            if book[10] == 1:
                read = "Read"
            
            shelf_id = Library.get_shelf_for_book(book[0], session["user_id"])[0]
            if book[0] not in library:
                library[book[0]] = {"title": book[1], "author": book[2], "pages": book[3], "color": book[4], "color_name": book[5], "publisher": book[6], "published_date": book[7], "fiction_nonfiction": fiction_nonfiction, "genre": book[9], "read": read, "isbn": book[11], "shelf_id": shelf_id}

    elif request.form.get("search_by") == "genre":
        logging.info(f"Searching books by GENRE {request.form.get('search_bar')}")
        results = Book.search_books_by_title(request.form.get("search_bar"), session["user_id"])

        for book in results:
            if book[8] == 0:
                fiction_nonfiction = "Nonfiction"
            if book[8] == 1:
                fiction_nonfiction = "Fiction"
            if book[10] == 0:
                read = "Not Read"
            if book[10] == 1:
                read = "Read"
            
            shelf_id = Library.get_shelf_for_book(book[0], session["user_id"])[0]
            if book[0] not in library:
                library[book[0]] = {"title": book[1], "author": book[2], "pages": book[3], "color": book[4], "color_name": book[5], "publisher": book[6], "published_date": book[7], "fiction_nonfiction": fiction_nonfiction, "genre": book[9], "read": read, "isbn": book[11], "shelf_id": shelf_id}

    elif request.form.get("search_by") == "color":
        logging.info(f"Searching books by COLOR {request.form.get('search_bar')}")
        results = Book.search_books_by_title(request.form.get("search_bar"), session["user_id"])

        for book in results:
            if book[8] == 0:
                fiction_nonfiction = "Nonfiction"
            if book[8] == 1:
                fiction_nonfiction = "Fiction"
            if book[10] == 0:
                read = "Not Read"
            if book[10] == 1:
                read = "Read"
            
            shelf_id = Library.get_shelf_for_book(book[0], session["user_id"])[0]
            if book[0] not in library:
                library[book[0]] = {"title": book[1], "author": book[2], "pages": book[3], "color": book[4], "color_name": book[5], "publisher": book[6], "published_date": book[7], "fiction_nonfiction": fiction_nonfiction, "genre": book[9], "read": read, "isbn": book[11], "shelf_id": shelf_id}

    return render_template("search_results.html", library=library)


@app.route("/add_shelf", methods=["POST"])
@login_required
def add_shelf():
    logging.info("==============================/nAdding Shelf/n==============================")
    if not request.form.get("shelf_number"):
        logging.error(f"Error : Shelf Number Not Entered")
        return error("Please enter shelf number to create new shelf")
    if Shelf.get_shelf_by_number(request.form.get("shelf_number"), session["user_id"]) is not None:
        logging.error("Shelf Number Already Exists")
        return error("Shelf number already exists")
    
    added_date = datetime.utcnow()
    logging.info(f"Current DateTime : {added_date}")

    Shelf.add_shelf(request.form.get("shelf_number"), added_date, session["user_id"])

    return redirect("/")


@app.route("/remove_shelf", methods=["POST"])
@login_required
def remove_shelf():
    logging.info("==============================/nRemoving Shelf/n==============================")
    Shelf.remove_shelf_by_num(int(request.form.get("remove_shelf_id")), session["user_id"])
    return redirect("/")


@app.route("/edit_shelf", methods=["POST"])
@login_required
def edit_shelf():
    logging.info("==============================/nEditing Shelf/n==============================")
    if not request.form.get("shelf_number"):
        logging.error("New Shelf Number Not Entered")
        return error("Please update shelf_number")
    if Shelf.get_shelf_by_number(request.form.get("shelf_number"), session["user_id"]) is not None:
        logging.error("Shelf Number Already Exists")
        return error("Shelf number already exists")
    
    Shelf.edit_shelf_number(request.form.get("current_shelf_number"), request.form.get("shelf_number"), session["user_id"])

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    # Check if request is POST
    if request.method == "POST":
        logging.info("==============================/nRegistering User/n==============================")
        # Check if form is filled out before submitting
        if not request.form.get("username"):
            logging.error("No Username Entered")
            return error("Please enter an username")
        if not request.form.get("email"):
            logging.error("No Email Entered")
            return error("Please enter an email")
        if not request.form.get("password"):
            logging.error("No Password Entered")
            return error("Please enter a password")
        if not request.form.get("verify"):
            logging.error("No Verification of Password Entered")
            return error("Please verify password")
        
        # Validate email and password meet requirments
        if not User.validate_email(request.form.get("email")):
            logging.error("Email is not valid format")
            return error("Email not valid")
        if not User.validate_password(request.form.get("password")):
            logging.error("Password is not valid format")
            return error("Please make the password more complex")
        
        # Verify passwords match
        hash = User.get_hash(request.form.get("password"))
        if not User.compare_passwords(hash, request.form.get("verify")):
            logging.error("Passwords do not match")
            return error("Passwords do not match")

        # Check if username and/or email already exist
        if User.get_user_by_username(request.form.get("username")) is not None:
            logging.error("Username Already Exists")
            return error("Username already exists")
        if User.get_user_by_email(request.form.get("email")) is not None:
            logging.error("Email Already Exists")
            return error("Email already exists")
        
        # Add user to the database
        User.add_user(request.form.get("username"), request.form.get("email"), hash, datetime.utcnow())

        # Assign user_id to session variable
        session["user_id"] = get_session_user(request.form.get("username"))
        logging.info(f"Session User ID : {session['user_id']}")

        return redirect("/")

    # Check if request is GET
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        logging.info("==============================/nLogging In User/n==============================")
        # Check for username and password fields being filled out
        if not request.form.get("username_email"):
            logging.error("Username or Email was not Entered")
            error("Please enter username or email")
        if not request.form.get("password"):
            logging.error("Password was not Entered")
            return error("Error connecting to database. Try again later.")
        
        # Check if username or email matches entry in database
        if not User.get_user_by_username(request.form.get("username_email")):
            logging.error("Username or Email does not Exists")
            return error("User does not exist")
        
        session["user_id"] = get_session_user(request.form.get("username_email"))
        logging.info(f"User ID : {session['user_id']}")

        # Check if password matches
        hash = User.get_user_hash_by_id(session["user_id"])[0]
        if not User.compare_passwords(hash, request.form.get("password")):
            logging.error("Password does not Match Password on File")
            session.clear()
            return error("Password does not match password on file")
        
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logging.info("Logging Out")
    session.clear()

    return redirect("/")


@app.route("/account")
@login_required
def account():
    return render_template("account.html")


@app.route("/edit_username", methods=["POST"])
@login_required
def edit_username():
    logging.info("==============================/nUpdating Username/n==============================")
    if not request.form.get("current_username"):
        logging.error("Current Username not entered")
        return error("Please enter current username to update username")
    if not request.form.get("new_username"):
        logging.error("New username not entered")
        return error("Please enter new username to update username")
    if User.get_user_by_username(request.form.get("new_username")) is not None:
        logging.error("Username already exists")
        return error("New username already exists")
    
    User.update_username(request.form.get("current_username"), request.form.get("new_username"), session["user_id"])
    return redirect("/account")


@app.route("/edit_email", methods=["GET", "POST"])
@login_required
def edit_email():
    logging.info("==============================/nUpdating Email/n==============================")
    if not request.form.get("current_email"):
        logging.error("Current Email not entered")
        return error("Please enter current email to update email")
    if not request.form.get("new_email"):
        logging.error("New email not entered")
        return error("Please enter new email to update email")
    if User.get_user_by_email(request.form.get("new_email")) is not None:
        logging.error("Email already exists")
        return error("New email already exists")
    
    User.update_username(request.form.get("current_email"), request.form.get("new_email"), session["user_id"])
    return redirect("/account")


@app.route("/edit_password", methods=["GET", "POST"])
@login_required
def edit_password():
    logging.info("==============================/nUpdating Password/n==============================")
    if not request.form.get("current_password"):
        logging.error("Current Password not entered")
        return error("Please enter current password to update password")
    if not request.form.get("new_password"):
        logging.error("New password not entered")
        return error("Please enter new password to update password")
    if not request.form.get("verify_password"):
        logging.error("Verification of new password not entered")
        return error("Please verify new password to update password")
    
    current_hash = User.get_user_hash_by_id(session["user_id"])[0]
    if not User.compare_passwords(current_hash, request.form.get("current_password")):
        logging.error(f"Current Hash {current_hash} does not match entered current password")
        return error("Entered current password does not match password on file")
    new_hash = User.get_hash(request.form.get("new_password"))
    if not User.compare_passwords(new_hash, request.form.get("verify_password")):
        logging.error("New password and verification password do not match")
        return error("Verification password must match new password")
    
    User.update_password(current_hash, new_hash, session["user_id"])
    return redirect("/account")


if __name__ == "__main__":
    app.run(debug=True)