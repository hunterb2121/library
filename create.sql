CREATE TABLE users (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    hash TEXT NOT NULL,
    created_date TEXT NOT NULL
);

CREATE TABLE books (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
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
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    number INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE books_shelf (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    bookshelf_id INTEGER NOT NULL,
    books_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (shelf_id) REFERENCES shelf (id),
    FOREIGN KEY (book_id) REFERENCES book (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);