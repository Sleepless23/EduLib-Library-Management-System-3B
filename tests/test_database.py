import sqlite3
from src import database

def test_initialize_db(test_db):
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}

    assert "books" in tables
    assert "students" in tables
    assert "loans" in tables

    conn.close()


def test_update_book(test_db):
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (isbn, title, author, genre, quantity) VALUES (?, ?, ?, ?, ?)",
        ("123", "Old Title", "Author A", "Genre A", 3)
    )
    conn.commit()
    book_id = cursor.lastrowid
    conn.close()

    database.update_book(book_id, "New Title", "New Author", "New Genre", 10)

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT title, author, genre, quantity FROM books WHERE id=?", (book_id,))
    result = cursor.fetchone()
    conn.close()

    assert result == ("New Title", "New Author", "New Genre", 10)


def test_delete_book(test_db):
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (isbn, title, author, genre, quantity) VALUES (?, ?, ?, ?, ?)",
        ("999", "Delete Me", "X", "Y", 1)
    )
    conn.commit()
    book_id = cursor.lastrowid
    conn.close()

    database.delete_book(book_id)

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
    result = cursor.fetchone()
    conn.close()

    assert result is None

