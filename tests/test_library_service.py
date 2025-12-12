import sqlite3
import pytest
from unittest.mock import patch
from src import library_service
from datetime import date, timedelta

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

    assert "No students" in captured.out or "===" in captured.out

def test_borrow_book_student_not_found(test_db, capsys):
    library_service.borrow_book("999999", 999)  # student doesn't exist
    out = capsys.readouterr().out
    assert "Student not found" in out


def test_borrow_book_not_existing_book(test_db, capsys):
    
    library_service.register_student("John", "MCC", "12-A", "0900")
    
    library_service.borrow_book("DOES-NOT-EXIST", 1)
    out = capsys.readouterr().out
    assert "Book not found" in out


def test_borrow_book_no_quantity(test_db, capsys):
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    
    cursor.execute("INSERT INTO books (isbn, title, author, genre, quantity) VALUES (?, ?, ?, ?, ?)",
                   ("B100", "ZeroBook", "Auth", "None", 0))

    
    cursor.execute("INSERT INTO students (name, school_name, grade_class, contact_info) VALUES (?, ?, ?, ?)",
                   ("John", "MCC", "12-A", "0900"))
    conn.commit()
    conn.close()

    library_service.borrow_book("B100", 1)
    out = capsys.readouterr().out
    assert "unavailable" in out


def test_borrow_book_success(test_db, capsys):
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO books (isbn, title, author, genre, quantity) VALUES (?, ?, ?, ?, ?)",
                   ("B200", "Borrowable Book", "Auth", "Fiction", 3))

    cursor.execute("INSERT INTO students (name, school_name, grade_class, contact_info) VALUES (?, ?, ?, ?)",
                   ("Jane", "MCC", "11-C", "0912"))
    conn.commit()
    conn.close()

    library_service.borrow_book("B200", 1)

    out = capsys.readouterr().out
    assert "Success" in out  

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM books WHERE isbn='B200'")
    qty_after = cursor.fetchone()[0]
    conn.close()

    assert qty_after == 2

def test_return_book_success(test_db, capsys):
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO books (isbn, title, author, genre, quantity) VALUES (?, ?, ?, ?, ?)",
                   ("RET1", "ReturnBook", "Auth", "Fiction", 1))
    cursor.execute("INSERT INTO students (name, school_name, grade_class, contact_info) VALUES (?, ?, ?, ?)",
                   ("Sam", "MCC", "10-B", "0999"))
    student_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO loans (book_id, student_id, borrow_date, due_date, status)
        VALUES (1, ?, ?, ?, 'BORROWED')
    """, (student_id, date.today().isoformat(), (date.today()+timedelta(days=7)).isoformat()))
    loan_id = cursor.lastrowid
    conn.commit()
    conn.close()

    library_service.return_book(loan_id)
    out = capsys.readouterr().out
    assert "Success" in out

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM loans WHERE id=?", (loan_id,))
    status = cursor.fetchone()[0]

    cursor.execute("SELECT quantity FROM books WHERE isbn='RET1'")
    qty_after = cursor.fetchone()[0]

    conn.close()

    assert status == "RETURNED"
    assert qty_after == 2
