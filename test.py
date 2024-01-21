from helpers import get_db_connection

db_con, db_cur = get_db_connection()

data = db_cur.execute("SELECT books_shelf.id, books_shelf.user_id, bookshelf.number, books.book_name, books.author, books.cover_color, books.publishing_house, books.fiction_nonfiction, books.genre, books.been_read, books.ISBN FROM books_shelf INNER JOIN bookshelf ON books_shelf.bookshelf_id = bookshelf.id INNER JOIN books ON books_shelf.books_id = books.id WHERE books_shelf.user_id = 1")
data = data.fetchall()

print(data)