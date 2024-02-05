import logging
import re
import webcolors

from database import execute_query, fetch_all, fetch_one
from werkzeug.security import check_password_hash, generate_password_hash


# Class for holding User information
class User:
    def __init__(self, user_id, username, email, hash, created_date):
        self._user_id = user_id
        self._username = username
        self._email = email
        self._hash = hash
        self._created_date = created_date

    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, new_user_id):
        self._user_id = new_user_id

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, new_username):
        self._username = new_username

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, new_email):
        self._email = new_email

    @property
    def hash(self):
        return self._hash
    
    @hash.setter
    def hash(self, new_hash):
        self._hash = new_hash

    @property
    def created_date(self):
        return self._created_date
    
    @created_date.setter
    def created_date(self, new_date):
        self._created_date = new_date

    @staticmethod
    def add_user(username, email, hash, created_date):
        query = "INSERT INTO users (username, email, hash, created_date) VALUES (?, ?, ?, ?)"
        parameters = (username, email, hash, created_date)

        try:
            execute_query(query, parameters)
            logging.info(f"User : {username} | {email} : created successfully")
        except Exception as e:
            logging.error(f"Error adding user : {username} | {email} : Exception: {e}")

    @staticmethod
    def get_user_by_id(user_id):
        query = "SELECT * FROM users WHERE id = ?"
        try:
            result = fetch_one(query, (user_id,))
            logging.info(f"Got user successfully : User Info {result} : User ID {user_id}")
            return result
        except Exception as e:
            logging.error(f"Error getting user: {e}")

    @staticmethod
    def get_user_by_username(username):
        query = "SELECT * FROM users WHERE username = ?"
        try:
            result = fetch_one(query, (username,))
            logging.info(f"Got user successfully : User Info {result} : Username {username}")
            return result
        except Exception as e:
            logging.error(f"Error getting user: {e}")

    @staticmethod
    def get_user_by_email(email):
        query = "SELECT * FROM users WHERE email = ?"
        try:
            result = fetch_one(query, (email,))
            logging.info(f"Got user successfully : User Info {result} : Email {email}")
            return result
        except Exception as e:
            logging.error(f"Error getting user: {e}")

    @staticmethod
    def get_user_id_by_username_email(username):
        query = "SELECT id FROM users WHERE username = ? OR email = ?"
        try:
            result = fetch_one(query, (username, username,))
            logging.info(f"Got user ID successfully : User ID {result} : Username {username}")
            return result
        except Exception as e:
            logging.error(f"Error getting user: {e}")

    @staticmethod
    def get_user_hash_by_id(user_id):
        query = "SELECT hash FROM users WHERE id = ?"
        try:
            result = fetch_one(query, (user_id,))
            logging.info(f"Got user hash successfully : Hash {result} : User ID {user_id}")
            return result
        except Exception as e:
            logging.error(f"Error getting hash: {e}")

    @staticmethod
    def get_user_hash_by_username(username):
        query = "SELECT hash FROM users WHERE username = ?"
        try:
            result = fetch_one(query, (username,))
            logging.info(f"Got user hash successfully : Hash {result} : Username {username}")
            return result
        except Exception as e:
            logging.error(f"Error getting hash: {e}")

    @staticmethod
    def get_user_hash_by_email(email):
        query = "SELECT hash FROM users WHERE email = ?"
        try:
            result = fetch_one(query, (email,))
            logging.info(f"Got user hash successfully : Hash {result} : Email {email}")
            return result
        except Exception as e:
            logging.error(f"Error getting hash: {e}")
    
    @staticmethod
    def update_username(current_username, new_username, user_id):
        query = "UPDATE users SET username = ? WHERE username = ? AND id = ?"
        parameters = (new_username, current_username, user_id,)
        try:
            execute_query(query, parameters)
            logging.info(f"Successfully updated username from {current_username} to {new_username}")
        except Exception as e:
            logging.error(f"Issue updating username from {current_username} to {new_username} : {e}")

    @staticmethod
    def update_email(current_email, new_email, user_id):
        query = "UPDATE users SET email = ? WHERE email = ? AND id = ?"
        parameters = (new_email, current_email, user_id,)
        try: 
            execute_query(query, parameters)
            logging.info(f"Successfully updated email from {current_email} to {new_email}")
        except Exception as e:
            logging.error(f"Issue updating email from {current_email} to {new_email} : {e}")

    @staticmethod
    def update_password(current_hash, new_hash, user_id):
        query = "UPDATE users SET hash = ? WHERE hash = ? AND id = ?"
        parameters = (new_hash, current_hash, user_id,)
        try:
            execute_query(query, parameters)
            logging.info(f"Successfully updated hash from {current_hash} to {new_hash}")
        except Exception as e:
            logging.error(f"Issue updating hash from {current_hash} to {new_hash} : {e}")

    @staticmethod
    def get_hash(password):
        return generate_password_hash(password)
    
    @staticmethod
    def compare_passwords(hash, password):
        return check_password_hash(hash, password)

    def save_user_to_database(self):
        query = "INSERT INTO users (username, email, hash, created_date) VALUES (?, ?, ?, ?)"
        parameters = (self._username, self._email, self._hash, self._created_date)

        try:
            execute_query(query, parameters)
            logging.info(f"Added user : {self._username} | {self._email} : successfully")
        except Exception as e:
            logging.error(f"Error adding user : {self._username} | {self._email} : {e}")

    # Regex from https://uibakery.io/regex-library
    @staticmethod
    def validate_email(email):
        pattern = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$" 
        if not re.match(pattern, email):
            logging.warning(f"Email does not meet standards : Email {email}")
            return False
        else:
            logging.info("Email validated successfully")
            return True

    # Regex from https://uibakery.io/regex-library
    @staticmethod
    def validate_password(password):
        pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        if not re.match(pattern, password):
            logging.warning(f"Password does not match standards")
            return False
        else:
            logging.info("Password validated successfully")
            return True


# Class for making book objects
class Book:
    def __init__(self, book_id, title, author, pages, cover_color, color_name, publisher, published_date, fiction_nonfiction, genre, been_read, isbn, added_date, user_id):
        self._book_id = book_id
        self._title = title
        self._author = author
        self._pages = pages
        self._cover_color = cover_color
        try:
            self._color_name = webcolors.hex_to_name(self._cover_color)
        except:
            self._color_name = None
        self._publisher = publisher
        self._published_date = published_date
        self._fiction_nonfiction = fiction_nonfiction
        self._genre = genre
        self._been_read = been_read
        self._isbn = isbn
        self._added_date = added_date
        self._user_id = user_id

    @property
    def book_id(self):
        return self._book_id
    
    @book_id.setter
    def book_id(self, new_book_id):
        self._book_id = new_book_id

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, new_title):
        self._title = new_title

    @property
    def author(self):
        return self._author
    
    @author.setter
    def author(self, new_author):
        self._author = new_author

    @property
    def pages(self):
        return self._pages
    
    @pages.setter
    def pages(self, new_pages):
        self._pages = new_pages

    @property
    def cover_color(self):
        return self._cover_color
    
    @cover_color.setter
    def cover_color(self, new_cover_color):
        self._cover_color = new_cover_color

    @property
    def color_name(self):
        return self._color_name
    
    @color_name.setter
    def color_name(self, new_color_name):
        self._color_name = new_color_name

    @property
    def publisher(self):
        return self._publisher
    
    @publisher.setter
    def publisher(self, new_publisher):
        self._publisher = new_publisher

    @property
    def published_date(self):
        return self._published_date
    
    @published_date.setter
    def published_date(self, new_published_date):
        self._published_date = new_published_date

    @property
    def fiction_nonfiction(self):
        return self._fiction_nonfiction
    
    @fiction_nonfiction.setter
    def fiction_nonfiction(self, new_fiction):
        self._fiction_nonfiction = new_fiction

    @property
    def genre(self):
        return self._genre
    
    @genre.setter
    def genre(self, new_genre):
        self._genre = new_genre

    @property
    def been_read(self):
        return self._been_read
    
    @been_read.setter
    def been_read(self, new_read):
        self._been_read = new_read

    @property
    def isbn(self):
        return self._isbn
    
    @isbn.setter
    def isbn(self, new_isbn):
        self._isbn = new_isbn

    @property
    def added_date(self):
        return self._added_date
    
    @added_date.setter
    def added_date(self, new_date):
        self._added_date = new_date

    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, new_user_id):
        self._user_id = new_user_id

    def save_book_to_database(self):
        query = "INSERT INTO books (title, author, pages, cover_color, color_name, publishing_house, published_date, fiction_nonfiction, genre, been_read, ISBN, added_date, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        parameters = (self._title, self._author, self._pages, self._cover_color, self._color_name, self._publisher, self._published_date, self._fiction_nonfiction, self._genre, self._been_read, self._isbn, self._added_date, self._user_id)

        try:
            execute_query(query, parameters)
            logging.info(f"Added book : {self._title} | {self._author} : successfully")
        except Exception as e:
            logging.error(f"Error adding book: {self._title} | {self._author} : {e}")

    @staticmethod
    def add_book(title, author, pages, cover_color, publisher, published_date, fiction_nonfiction, genre, been_read, isbn, added_date, user_id):
        query = "INSERT INTO books (title, author, pages, cover_color, color_name, publishing_house, published_date, fiction_nonfiction, genre, been_read, ISBN, added_date, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        try:
            color_name = webcolors.hex_to_name(cover_color)
        except:
            color_name = None
        parameters = (title, author, pages, cover_color, color_name, publisher, published_date, fiction_nonfiction, genre, been_read, isbn, added_date, user_id)

        try:
            execute_query(query, parameters)
            logging.info(f"Added book : {title} | {author} : successfully")
        except Exception as e:
            logging.error(f"Error adding book: {title} | {author} : {e}")

    @staticmethod
    def edit_book(book_id, editing, new_value, user_id):
        query = f"UPDATE books SET {editing} = ? WHERE id = ? AND user_id = ?"
        parameters = (new_value, book_id, user_id,)
        try:
            execute_query(query, parameters)
            logging.info(f"Updated book successfully : Book ID {book_id} : Editing {editing} : New Value {new_value} : User ID {user_id}")
        except Exception as e:
            logging.error(f"Error updating {editing} field: {e}")

    @staticmethod
    def delete_book_by_id(book_id, user_id):
        remove_from_books_query = "DELETE FROM books WHERE id = ? AND user_id = ?"
        remove_from_books_parameters = (book_id, user_id,)
        try:
            execute_query(remove_from_books_query, remove_from_books_parameters)
            logging.info(f"Deleted book successfully : Book ID {book_id} : User ID {user_id}")
        except Exception as e:
            logging.error(f"Error deleting book: {e} | Issue with either {book_id} or {user_id}")

    @staticmethod
    def get_books_by_user(user_id):
        query = "SELECT * FROM books WHERE user_id = ?"

        try:
            results = fetch_all(query, (user_id,))
            logging.info(f"Successfully got books : Books {results} : User ID {user_id}")
            return results
        except Exception as e:
            logging.error(f"Error getting books: {e}")
    
    @staticmethod
    def get_books_by_id(book_id):
        query = "SELECT * FROM books WHERE id = ?"

        try:
            results = fetch_one(query, (book_id,))
            logging.info(f"Successfully got books : Book {results} : Book ID {book_id}")
            return results
        except Exception as e:
            logging.error(f"Error getting books: {e}")

    @staticmethod
    def get_book_id_by_title_added_date(title, added_date, user_id):
        query = "SELECT id FROM books WHERE title = ? AND added_date = ? AND user_id = ?"
        parameters = (title, added_date, user_id)
        try:
            result = fetch_one(query, parameters)
            logging.info(f"Successfully got book : Title {title} : Added Date {added_date} : User ID {user_id}")
            return result
        except Exception as e:
            logging.warning(f"Error getting book: {title} : {e}")

    @staticmethod
    def search_books_by_title(title, user_id):
        query = "SELECT * FROM books WHERE title LIKE ? AND user_id = ?"
        parameters = ("%" + str(title).lower() + "%", user_id,)

        try:
            results = fetch_all(query, parameters)
            logging.info(f"Successfully searching books by title : Results {results} : Title Search {title}")
            return results
        except Exception as e:
            logging.warning(f"Error searching books by title: {e}")

    @staticmethod
    def search_books_by_genre(genre, user_id):
        query = "SELECT * FROM books WHERE genre LIKE ? AND user_id = ?"
        parameters = ("%" + str(genre).lower() + "%", user_id,)

        try:
            results = fetch_all(query, parameters)
            logging.info(f"Successfully searching books by genre : Results {results} : Genre Search {genre}")
            return results
        except Exception as e:
            logging.warning(f"Error searching books by genre: {e}")

    @staticmethod
    def search_books_by_author(author, user_id):
        query = "SELECT * FROM books WHERE author LIKE ? AND user_id = ?"
        parameters = ("%" + str(author).lower() + "%", user_id,)

        try:
            results = fetch_all(query, parameters)
            logging.info(f"Successfully searching books by author : Results {results} : Author Search {author}")
            return results
        except Exception as e:
            logging.warning(f"Error searching books by author: {e}")

    @staticmethod
    def search_books_by_color(color, user_id):
        query = "SELECT * FROM books WHERE color_name LIKE ? AND user_id = ?"
        parameters = ("%" + str(color).lower() + "%", user_id,)

        try:
            results = fetch_all(query, parameters)
            logging.info(f"Successfully searching books by cover color : Results {results} : Color Search {color}")
            return results
        except Exception as e:
            logging.warning(f"Error searching books: {e}")

    @staticmethod
    def sort_books(user_id, sort_by, ascending=True):
        order = "ASC" if ascending else "DESC"
        query = f"SELECT * FROM books WHERE user_id = ? ORDER BY {sort_by} {order}"
        parameters = (user_id,)

        try:
            results = fetch_all(query, parameters)
            logging.info(f"Successfully got sorted books : Results {results} : User ID {user_id} : Sorting by {sort_by} : Ascending? {ascending}")
            return results
        except Exception as e:
            logging.error(f"Error sorting books: {e}")

    @staticmethod
    def move_to_shelf(title, user_id, added_date, current_shelf, new_shelf):
        book_query = "SELECT id FROM books WHERE title = ? AND user_id = ? AND added_date = ?"
        book_parameters = (title, user_id, added_date,)
        current_shelf_query = "SELECT id FROM bookshelf WHERE number = ? AND user_id = ?"
        current_shelf_parameters = (current_shelf, user_id,)
        new_shelf_query = "SELECT id FROM bookshelf WHERE number = ? AND user_id = ?"
        new_shelf_parameters = (new_shelf, user_id,)
        try:
            get_book = fetch_one(book_query, book_parameters)
            logging.info(f"Successfully got book to move : Book {get_book}")
        except Exception as e:
            logging.error(f"Error fetching book to move: {e}")
        try:
            get_current_shelf = fetch_one(current_shelf_query, current_shelf_parameters)
            logging.info(f"Successfully got current shelf : Current Shelf {get_current_shelf}")
        except Exception as e:
            logging.error(f"Error fetching current shelf: {e}")
        try:
            get_new_shelf = fetch_one(new_shelf_query, new_shelf_parameters)
            logging.info(f"Successfully got shelf to move book to : New Shelf {get_new_shelf}")
        except Exception as e:
            logging.error(f"Error fetching new shelf: {e}")

        book_id = get_book[0]
        logging.info(f"Book ID {book_id}")
        origin_shelf_id = get_current_shelf[0]
        logging.info(f"Current Shelf {origin_shelf_id}")
        destination_shelf_id = get_new_shelf[0]
        logging.info(f"New Shelf {destination_shelf_id}")

        move_query = "UPDATE books_shelf SET bookshelf_id = ? WHERE books_id = ? AND bookshelf_id = ? AND user_id = ?"
        move_parameters = (destination_shelf_id, book_id, origin_shelf_id, user_id,)
        try:
            execute_query(move_query, move_parameters)
            logging.info(f"Successfully moved book from old shelf to new shelf")
        except Exception as e:
            logging.error(f"Error moving book to new shelf: {e}")


# Shelf Object
class Shelf:
    def __init__(self, shelf_id, shelf_number, added_date, user_id):
        self._shelf_id = shelf_id
        self._shelf_number = shelf_number
        self._added_date = added_date
        self._user_id = user_id
        self._books = []

    @property 
    def shelf_id(self):
        return self._shelf_id
    
    @shelf_id.setter
    def shelf_id(self, new_shelf_id):
        self._shelf_id = new_shelf_id

    @property
    def shelf_number(self):
        return self._shelf_number
    
    @shelf_number.setter
    def shelf_number(self, new_shelf_number):
        self._shelf_number = new_shelf_number

    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, new_user_id):
        self._user_id = new_user_id

    @property
    def books(self):
        return self._books
    
    @books.setter
    def books(self, new_books):
        self._books = new_books

    def save_shelf_to_database(self):
        query = "INSERT INTO bookshelf (number, added_date, user_id) VALUES (?, ?, ?)"
        parameters = (self._shelf_number, self._added_date, self._user_id,)

        try:
            execute_query(query, parameters)
            logging.info(f"Successfully saved shelf to database : Shelf Number {self._shelf_number} : Added Date {self._added_date} : User ID {self._user_id}")
        except Exception as e:
            logging.error(f"Error adding shelf: {e}")

    @staticmethod
    def add_shelf(number, added_date, user_id):
        query = "INSERT INTO bookshelf (number, added_date, user_id) VALUES (?, ?, ?)"
        parameters = (number, added_date, user_id,)

        try:
            execute_query(query, parameters)
            logging.info(f"Successfully saved shelf to database : Shelf Number {number} : Added Date {added_date} : User ID {user_id}")
        except Exception as e:
            logging.error(f"Error adding shelf: {e}")

    @staticmethod
    def edit_shelf_number(shelf_id, new_number, user_id):
        query = "UPDATE bookshelf SET number = ? WHERE id = ? AND user_id = ?"
        parameters = (new_number, shelf_id, user_id,)

        try:
            execute_query(query, parameters)
            logging.info(f"Successfully edited shelf number : Shelf ID {shelf_id} : New Number {new_number} : User ID {user_id}")
        except Exception as e:
            logging.warning(f"Error updating shelf number: {e}")

    @staticmethod
    def remove_shelf_by_id(shelf_id, user_id):
        query = "DELETE FROM bookshelf WHERE id = ? AND user_id = ?"
        parameters = (shelf_id, user_id,)
        try:
            execute_query(query, parameters)
            logging.info(f"Successfully deleted shelf : shelf ID {shelf_id} : User ID {user_id}")
        except Exception as e:
            logging.error(f"Error removing shelf ID {shelf_id}: {e}")

    @staticmethod
    def remove_shelf_by_num(shelf_num, user_id):
        query = "DELETE FROM bookshelf WHERE number = ? AND user_id = ?"
        parameters = (shelf_num, user_id,)
        try:
            execute_query(query, parameters)
            logging.info(f"Successfully deleted shelf : Shelf Number {shelf_num} : User ID {user_id}")
        except Exception as e:
            logging.error(f"Error removing shelf number {shelf_num} : {e}")

    @staticmethod
    def get_shelf_by_user(user_id):
        query = "SELECT * FROM bookshelf WHERE user_id = ?"
        try:
            results = fetch_all(query, (user_id,))
            logging.info(f"Successfully got shelves : Results {results} : User ID {user_id}")
            return results
        except Exception as e:
            logging.error(f"Error getting shelves: {e}")

    @staticmethod
    def get_shelf_by_id(shelf_id):
        query = "SELECT * FROM bookshelf WHERE id = ?"
        try:
            results = fetch_one(query, (shelf_id,))
            logging.info(f"Successfully got shelf : Results {results} : Shelf ID {shelf_id}")
            return results
        except Exception as e:
            logging.error(f"Error getting shelves: {e}")

    @staticmethod
    def get_shelf_by_number(shelf_num, user_id):
        query = "SELECT * FROM bookshelf WHERE number = ? AND user_id = ?"
        parameters = (shelf_num, user_id,)
        try:
            results = fetch_one(query, parameters)
            logging.info(f"Successfully got shelf : Results {results} : Shelf Number {shelf_num} : User ID {user_id}")
            return results
        except Exception as e:
            logging.error(f"Error getting shelves: {e}")

    @staticmethod
    def get_shelf_number(shelf_id, user_id):
        query = "SELECT number FROM bookshelf WHERE id = ? AND user_id = ?"
        parameters = (shelf_id, user_id,)

        try:
            result = fetch_one(query, parameters)
            logging.info(f"Successfully got shelf number : Result {result} : Shelf ID {shelf_id} : User ID {user_id}")
            return result
        except Exception as e:
            logging.error(f"Error getting shelf number: {e}")

    @staticmethod
    def add_book_to_shelf_by_id(shelf_id, book_id, user_id):
        query = "INSERT INTO books_shelf (bookshelf_id, books_id, user_id) VALUES (?, ?, ?)"
        parameters = (shelf_id, book_id, user_id,)
        try:
            execute_query(query, parameters)
            logging.info(f"Successfully added book to shelf : Shelf ID {shelf_id} : Book ID {book_id} : User ID {user_id}")
        except Exception as e:
            logging.error(f"Error adding book to shelf: {e}")

    @staticmethod
    def add_book_to_shelf_by_num(shelf_num, book_id, user_id):
        get_shelf_id_num_query = "SELECT id FROM bookshelf WHERE number = ? AND user_id = ?"
        get_shelf_id_num_parameters = (shelf_num, user_id,)
        try:
            shelf_id = fetch_one(get_shelf_id_num_query, get_shelf_id_num_parameters)
            shelf_id = shelf_id[0]
            logging.info(f"Got shelf ID {shelf_id} from shelf number {shelf_num}")
            add_book_shelf_query = "INSERT INTO books_shelf (bookshelf_id, books_id, user_id) VALUES (?, ?, ?)"
            add_book_shelf_parameters = (shelf_id, book_id, user_id)
            try:
                execute_query(add_book_shelf_query, add_book_shelf_parameters)
                logging.info(f"Added book ID {book_id} to shelf ID {shelf_id} by shelf number {shelf_num}")
            except Exception as e:
                logging.error(f"Cannot add book ID {book_id} to shelf ID {shelf_id} by shelf num {shelf_num} : {e}")
        except Exception as e:
            logging.error(f"Cannot get shelf ID from Number : {e}")

    @staticmethod
    def remove_book_from_shelf(shelf_id, book_id, user_id):
        query = "DELETE FROM books_shelf WHERE bookshelf_id = ? AND books_id = ? AND user_id = ?"
        parameters = (shelf_id, book_id, user_id,)
        try:
            execute_query(query, parameters)
            logging.info(f"Successfully removed book from shelf : Shelf ID {shelf_id} : Book ID {book_id} : User ID {user_id}")
        except Exception as e:
            logging.error(f"Error removing book from shelf: {e}")


# Class for holding dictionaries for shelf objects and book objects
class Library:
    def __init__(self):
        self._shelves = []
        self._books = []

    @property
    def shelves(self):
        return self._shelves
    
    @shelves.setter
    def shelves(self, new_shelves):
        self._shelves = new_shelves

    @property
    def books(self):
        return self._books
    
    @books.setter
    def books(self, new_books):
        self._books = new_books

    def add_book_to_library(self, book):
        self._books.append(book)

    def add_shelf_to_library(self, shelf):
        self._shelves.append(shelf)

    def get_books_in_library(self):
        return self._books
    
    def get_shelves_in_library(self):
        return self._shelves
    
    def remove_books_from_library(self, book):
        self._books.remove(book)

    def remove_shelf_from_library(self, shelf):
        self._shelves.remove(shelf)

    # Get the shelf that a book is on in books_shelf
    @ staticmethod
    def get_shelf_for_book(book_id, user_id):
        query = "SELECT bookshelf_id FROM books_shelf WHERE books_id = ? AND user_id = ?"
        parameters = (book_id, user_id,)
        try:
            result = fetch_one(query, parameters)
            logging.info(f"Successfully got shelf for book : Result {result} : Book ID {book_id} : User ID {user_id}")
            return result
        except Exception as e:
            logging.error(f"Error getting shelf: {e}")

    # Get a list of books that are on a shelf in books_shelf
    @staticmethod
    def get_books_on_shelf(shelf_id, user_id):
        query = "SELECT books_id FROM books_shelf WHERE bookshelf_id = ? AND user_id = ?"
        parameters = (shelf_id, user_id,)
        try:
            results = fetch_all(query, parameters)
            logging.info(f"Successfully got books on shelf : Results {results} : Shelf ID {shelf_id} : User ID {user_id}")
            return results
        except Exception as e:
            logging.error(f"Error getting books: {e}")
