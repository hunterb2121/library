DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS bookshelf;
DROP TABLE IF EXISTS books_shelf;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    created_date TEXT NOT NULL
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    pages INTEGER NOT NULL,
    cover_color TEXT NOT NULL,
    color_name TEXT NOT NULL,
    publishing_house TEXT NOT NULL,
    published_date TEXT NOT NULL,
    fiction_nonfiction INTEGER NOT NULL,
    genre TEXT NOT NULL,
    been_read INTEGER NOT NULL,
    ISBN TEXT NOT NULL,
    added_date TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE bookshelf (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number INTEGER NOT NULL UNIQUE,
    added_date TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE books_shelf (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bookshelf_id INTEGER NOT NULL,
    books_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (bookshelf_id) REFERENCES bookshelf (id) ON DELETE CASCADE,
    FOREIGN KEY (books_id) REFERENCES books (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE INDEX idxusername ON users (username);
CREATE INDEX idxemail ON users (email);

CREATE INDEX idxbook_users ON books (user_id);
CREATE INDEX idxtitle ON books (title);
CREATE INDEX idxauthor ON books (author);
CREATE INDEX idxgenre ON books (genre);
CREATE INDEX idxcolor_name ON books (color_name);

CREATE INDEX idxshelf_number ON bookshelf (number);