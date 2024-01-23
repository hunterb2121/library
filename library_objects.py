from database import execute_query, fetch_all, fetch_one


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


# Class for making book objects
class Book:
    ...


# Class for holding User information
class User:
    ...


# Class for holding dictionaries for shelf objects and book objects
class Library:
    ...