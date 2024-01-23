from helpers import get_db_connection

db_con, db_cur = get_db_connection()

shelf_number = 1
book_title = "book1"
book_author = "author"
color = "color"
publisher = "publisher"
fiction_nonfiction = "fiction"
genre = "genre"
read_not_read = "read"
isbn = 65479841

if fiction_nonfiction == "fiction":
    fiction_nonfiction = 1
elif fiction_nonfiction == "nonfiction":
    fiction_nonfiction = 0

if read_not_read == "read":
    been_read = 1
elif read_not_read == "not_read":
    been_read = 0

db_cur.execute("INSERT INTO books (book_name, author, cover_color, publishing_house, fiction_nonfiction, genre, been_read, ISBN, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (book_title, book_author, color, publisher, fiction_nonfiction, genre, been_read, isbn, 1,))
db_con.commit()
book_id = db_cur.execute("SELECT id FROM books WHERE book_name = ? AND user_id = ?", (book_title, 1,))
book_id = book_id.fetchone()[0]
print(book_id)
bookshelf_id = db_cur.execute("SELECT id FROM bookshelf WHERE number = ? AND user_id = ?", (shelf_number, 1,))
bookshelf_id = bookshelf_id.fetchone()[0]
print(bookshelf_id)
db_cur.execute("INSERT INTO books_shelf (bookshelf_id, books_id, user_id) VALUES (?, ?, ?)", (bookshelf_id, book_id, 1,))
books_shelf = db_cur.execute("SELECT id FROM books_shelf WHERE bookshelf_id = ? AND books_id = ? AND user_id = ?", (bookshelf_id, book_id, 1))
books_shelf = books_shelf.fetchone()[0]
print(books_shelf)
db_con.commit()
db_cur.close()
