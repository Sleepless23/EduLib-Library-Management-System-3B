import sqlite3
import pytest
from unittest.mock import patch
from src import library_service

def test_add_book(test_db):
    library_service.add_book("111", "Test Book", "John", "Fiction", 5)

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT title, author, genre, quantity FROM books WHERE isbn='111'")
    result = cursor.fetchone()
    conn.close()

    assert result == ("Test Book", "John", "Fiction", 5)


@patch("src.library_service.requests.get")
def test_add_book_with_isbn(mock_req, test_db):

    mock_req.return_value.json.return_value = {
        "items": [{
            "volumeInfo": {
                "title": "API Book",
                "authors": ["Google"],
                "categories": ["Tech"]
            }
        }]
    }

    library_service.add_book_with_isbn("555", 2)

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT title, author, genre, quantity FROM books WHERE isbn='555'")
    result = cursor.fetchone()
    conn.close()

    assert result == ("API Book", "Google", "Tech", 2)


def test_register_and_edit_student(test_db):
    library_service.register_student("Alice", "MCC", "12-B", "091234")

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM students WHERE name='Alice'")
    student_id = cursor.fetchone()[0]
    conn.close()

    library_service.edit_student(student_id, name="Alice Updated")

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM students WHERE id=?", (student_id,))
    result = cursor.fetchone()[0]
    conn.close()

    assert result == "Alice Updated"


def test_show_students_no_crash(test_db, capsys):
    library_service.show_students()
    captured = capsys.readouterr()

    # Should not crash even if empty
    assert "No students" in captured.out or "===" in captured.out
