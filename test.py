from helpers import get_db_connection

db_con, db_cur = get_db_connection()

shelves = db_cur.execute("SELECT number FROM bookshelf WHERE user_id = ?", (1,))
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
                library[shelf[0]].append({"title": book[4], "author": book[5], "color": book[6], "publisher": book[7], "fiction_nonfiction": fiction_nonfiction, "genre": book[9], "read": read, "isbn": book[11]})
            else:
                library[shelf[0]] = [{"title": book[4], "author": book[5], "color": book[6], "publisher": book[7], "fiction_nonfiction": fiction_nonfiction, "genre": book[9], "read": read, "isbn": book[11]}]

print(library)