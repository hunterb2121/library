from database import execute_query, fetch_all, fetch_one
from datetime import datetime


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

        def save_user_to_database(self):
            query = "INSERT INTO users (username, email, hash, created_date) VALUES (?, ?, ?, ?)"
            parameters = (self._username, self._email, self._hash, self._created_date)

            try:
                execute_query(query, parameters)
                print("Added user successfully")
            except Exception as e:
                print(f"Error adding user: {e}")


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


# Shelf Object
class Shelf:
    def __init__(self, shelf_id, shelf_number, user_id):
        self._shelf_id = shelf_id
        self._shelf_number = shelf_number
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

    def get_initial_books(self):
        books_id_list = fetch_all("SELECT books_id FROM books_shelf WHERE bookshelf_id = ? AND user_id = ?", (self._shelf_id, self._user_id,))

        for book in books_id_list:
            self._books.append(book[0])


# Class for holding dictionaries for shelf objects and book objects
class Library:
    ...