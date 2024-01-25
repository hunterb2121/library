from library_objects import Book, Library, Shelf, User

user_library = Library()
user_books = Book.get_books_by_user(1)
user_shelves = Shelf.get_shelf_by_user(1)

for book in user_books:
    user_library.add_book_to_library(book)

for shelf in user_shelves:
    user_library.add_shelf_to_library(shelf)

shelves = user_library.get_shelves_in_library()
books = user_library.get_books_in_library()

print(shelves)
print(books)