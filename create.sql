CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    hash TEXT NOT NULL,
    created_date TEXT NOT NULL
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_name TEXT NOT NULL,
    author TEXT NOT NULL,
    cover_color TEXT NOT NULL,
    publishing_house TEXT NOT NULL,
    fiction_nonfiction INTEGER NOT NULL,
    genre TEXT NOT NULL,
    been_read INTEGER NOT NULL,
    ISBN TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE bookshelf (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE books_shelf (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bookshelf_id INTEGER NOT NULL,
    books_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (bookshelf_id) REFERENCES bookshelf (id),
    FOREIGN KEY (books_id) REFERENCES books (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);