from library_objects import Book, Library, Shelf, User

user_library = Library()
user_books = Book.get_books_by_user(1)
user_shelves = Shelf.get_shelf_by_user(1)

for book in user_books:
    user_library.add_book_to_library(book)

for shelf in user_shelves:
    user_library.add_shelf_to_library(shelf)

print(user_library.get_books_in_library())

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
        book_shelves[shelf_id].append({"title": book[1], "author": book[2], "pages": book[3], "color": book[4], "publisher": book[5], "published_date": book[6], "genre": book[8], "read": read, "isbn": book[10], "added_date": book[11]})
    else:
        book_shelves[shelf_id] = [{"title": book[1], "author": book[2], "pages": book[3], "color": book[4], "publisher": book[5], "published_date": book[6], "genre": book[8], "read": read, "isbn": book[10], "added_date": book[11]}]
    
print(book_shelves)