from database import execute_query, fetch_all, fetch_one
import re
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
            print("Added user successfully")
        except Exception as e:
            print(f"Error adding user: {e}")

    @staticmethod
    def get_user_by_id(user_id):
        query = "SELECT * FROM users WHERE id = ?"
        try:
            result = fetch_one(query, (user_id,))
            return result
        except Exception as e:
            print(f"Error getting user: {e}")

    @staticmethod
    def get_user_by_username(username):
        query = "SELECT * FROM users WHERE username = ?"
        try:
            result = fetch_one(query, (username,))
            return result
        except Exception as e:
            print(f"Error getting user: {e}")

    @staticmethod
    def get_user_by_email(email):
        query = "SELECT * FROM users WHERE email = ?"
        try:
            result = fetch_one(query, (email,))
            return result
        except Exception as e:
            print(f"Error getting user: {e}")

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
            print("Added user successfully")
        except Exception as e:
            print(f"Error adding user: {e}")

    @staticmethod
    def validate_email(email):
        pattern = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$" 
        if not re.match(pattern, email):
            return False
        else:
            return True

    @staticmethod
    def validate_password(password):
        pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        if not re.match(pattern, password):
            return False
        else:
            return True


# Class for making book objects
class Book:
    def __init__(self, book_id, title, author, pages, cover_color, publisher, published_date, fiction_nonfiction, genre, been_read, isbn, added_date, user_id):
        self._book_id = book_id
        self._title = title
        self._author = author
        self._pages = pages
        self._cover_color = cover_color
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
        query = ("INSERT INTO books (title, author, pages, cover_color, publishing_house, published_date, fiction_nonfiction, genre, been_read, ISBN, added_date, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        parameters = (self._title, self._author, self._pages, self._cover_color, self._publisher, self._published_date, self._fiction_nonfiction, self._genre, self._been_read, self._isbn, self._added_date, self._user_id)

        try:
            execute_query(query, parameters)
            print("Added book successfully")
        except Exception as e:
            print(f"Error adding book: {e}")

    @staticmethod
    def add_book(title, author, pages, cover_color, publisher, published_date, fiction_nonfiction, genre, been_read, isbn, added_date, user_id):
        query = ("INSERT INTO books (title, author, pages, cover_color, publishing_house, published_date, fiction_nonfiction, genre, been_read, ISBN, added_date, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        parameters = (title, author, pages, cover_color, publisher, published_date, fiction_nonfiction, genre, been_read, isbn, added_date, user_id)

        try:
            execute_query(query, parameters)
            print("Added book successfully")
        except Exception as e:
            print(f"Error adding book: {e}")

    @staticmethod
    def get_books_by_user(user_id):
        query = "SELECT * FROM books WHERE user_id = ?"

        try:
            results = fetch_all(query, (user_id,))
            return results
        except Exception as e:
            print(f"Error getting books: {e}")
    
    @staticmethod
    def get_books_by_id(book_id):
        query = "SELECT * FROM books WHERE id = ?"

        try:
            results = fetch_one(query, (book_id,))
            return results
        except Exception as e:
            print(f"Error getting books: {e}")

    @staticmethod
    def search_books_by_title(title):
        query = "SELECT * FROM books WHERE title LIKE ?"
        parameters = ("%" + title + "%",)

        try:
            results = fetch_all(query, parameters)
            return results
        except Exception as e:
            print("Error searching books: {e}")

    @staticmethod
    def search_books_by_genre(genre):
        query = "SELECT * FROM books WHERE genre LIKE ?"
        parameters = ("%" + genre + "%",)

        try:
            results = fetch_all(query, parameters)
            return results
        except Exception as e:
            print("Error searching books: {e}")

    @staticmethod
    def search_books_by_author(author):
        query = "SELECT * FROM books WHERE author LIKE ?"
        parameters = ("%" + author + "%",)

        try:
            results = fetch_all(query, parameters)
            return results
        except Exception as e:
            print("Error searching books: {e}")

    @staticmethod
    def search_books_by_color(cover_color):
        query = "SELECT * FROM books WHERE cover_color LIKE ?"
        parameters = ("%" + cover_color + "%",)

        try:
            results = fetch_all(query, parameters)
            return results
        except Exception as e:
            print("Error searching books: {e}")

    @staticmethod
    def sort_books(user_id, sort_by, ascending=True):
        order = "ASC" if ascending else "DESC"
        query = f"SELECT * FROM books WHERE user_id = ? ORDER BY {sort_by} {order}"
        parameters = (user_id,)

        try:
            results = fetch_all(query, parameters)
            return results
        except Exception as e:
            print(f"Error sorting books: {e}")

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
        except Exception as e:
            print(f"Error fetching book: {e}")
        try:
            get_current_shelf = fetch_one(current_shelf_query, current_shelf_parameters)
        except Exception as e:
            print(f"Error fetching current shelf: {e}")
        try:
            get_new_shelf = fetch_one(new_shelf_query, new_shelf_parameters)
        except Exception as e:
            print(f"Error fetching new shelf: {e}")

        book_id = get_book[0]
        origin_shelf_id = get_current_shelf[0]
        destination_shelf_id = get_new_shelf[0]

        move_query = "UPDATE books_shelf SET bookshelf_id = ? WHERE books_id = ? AND bookshelf_id = ? AND user_id = ?"
        move_parameters = (destination_shelf_id, book_id, origin_shelf_id, user_id,)
        try:
            execute_query(move_query, move_parameters)
        except Exception as e:
            print(f"Error moving book to new shelf: {e}")


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
        except Exception as e:
            print(f"Error adding shelf: {e}")

    @staticmethod
    def add_shelf(number, added_date, user_id):
        query = "INSERT INTO bookshelf (number, added_date, user_id) VALUES (?, ?, ?)"
        parameters = (number, added_date, user_id,)

        try:
            execute_query(query, parameters)
        except Exception as e:
            print(f"Error adding shelf: {e}")

    @staticmethod
    def get_shelf_by_user(user_id):
        query = "SELECT * FROM bookshelf WHERE user_id = ?"
        try:
            results = fetch_all(query, (user_id,))
            return results
        except Exception as e:
            print(f"Error getting shelves: {e}")

    @staticmethod
    def get_shelf_by_id(shelf_id):
        query = "SELECT * FROM bookshelf WHERE id = ?"
        try:
            results = fetch_all(query, (shelf_id,))
            return results
        except Exception as e:
            print(f"Error getting shelves: {e}")

    @staticmethod
    def get_shelf_by_number(shelf_num, user_id):
        query = "SELECT * FROM bookshelf WHERE number = ? AND user_id = ?"
        parameters = (shelf_num, user_id,)
        try:
            results = fetch_one(query, parameters)
            return results
        except Exception as e:
            print(f"Error getting shelves: {e}")

    @staticmethod
    def add_book_to_shelf(shelf_id, book_id, user_id):
        query = "INSERT INTO books_shelf (bookshelf_id, books_id, user_id) VALUES (?, ?, ?)"
        parameters = (shelf_id, book_id, user_id,)
        try:
            execute_query(query, parameters)
        except Exception as e:
            print(f"Error adding book to shelf: {e}")

    @staticmethod
    def remove_book_from_shelf(shelf_id, book_id, user_id):
        query = "DELETE FROM books_shelf WHERE bookshelf_id = ? AND books_id = ? AND user_id = ?"
        parameters = (shelf_id, book_id, user_id,)
        try:
            execute_query(query, parameters)
        except Exception as e:
            print(f"Error removing book from shelf: {e}")


# Class for holding dictionaries for shelf objects and book objects
class Library:
    def __init__(self):
        self._shelves = []
        self._books = []

    def add_book_to_library(self, book_info):
        self._books.append(book_info)

    def add_shelf_to_library(self, shelf_info):
        self._shelves.append(shelf_info)

    def get_books_in_library(self):
        return self._books
    
    def get_shelves_in_library(self):
        return self._shelves
    
    def remove_books_from_library(self, book_info):
        self._books.remove(book_info)

    def remove_shelf_from_library(self, shelf_info):
        self._shelves.remove(shelf_info)
