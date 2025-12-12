import sqlite3
import os
from datetime import date, timedelta
from src import library_service
from src.reports import fetch_overdue_loans, export_overdue_to_csv, export_overdue_to_pdf

def test_fetch_overdue_loans(test_db):
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO books (isbn, title, author, genre, quantity) VALUES (?, ?, ?, ?, ?)",
                   ("O1", "Overdue Book", "Auth", "Fiction", 1))
    cursor.execute("INSERT INTO students (name, school_name, grade_class, contact_info) VALUES (?, ?, ?, ?)",
                   ("LateKid", "MCC", "12-A", "0900"))
    student_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO loans (book_id, student_id, borrow_date, due_date, status)
        VALUES (1, ?, ?, ?, 'BORROWED')
    """, (student_id, date.today().isoformat(), (date.today()-timedelta(days=1)).isoformat()))

    conn.commit()
    conn.close()

    rows = fetch_overdue_loans()
    assert len(rows) == 1
    assert rows[0]["title"] == "Overdue Book"


def test_export_overdue_to_csv(tmp_path):
    rows = [{
        "loan_id": 1,
        "title": "Book",
        "isbn": "X1",
        "student_name": "A",
        "grade_class": "12-A",
        "school_name": "MCC",
        "borrow_date": "2024-01-01",
        "due_date": "2024-01-05",
    }]

    filename = tmp_path / "overdue.csv"
    res = export_overdue_to_csv(rows, filename)

    assert os.path.exists(res)


def test_export_pdf_no_reportlab(monkeypatch, tmp_path):
    """Force PDF_AVAILABLE=False to test fallback behavior"""
    monkeypatch.setattr("src.reports.PDF_AVAILABLE", False)

    rows = [{"loan_id": 1, "title": "B", "student_name": "X", "due_date": "2024-01-01"}]
    filename = tmp_path / "overdue.pdf"

    res = export_overdue_to_pdf(rows, filename)
    assert res is None

def test_report_most_borrowed_books(test_db, capsys):
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO books (isbn, title, author, genre, quantity) VALUES (?, ?, ?, ?, ?)",
                   ("B1", "Book A", "Author A", "Fiction", 5))
    cursor.execute("INSERT INTO books (isbn, title, author, genre, quantity) VALUES (?, ?, ?, ?, ?)",
                   ("B2", "Book B", "Author B", "SciFi", 5))

    cursor.execute("INSERT INTO students (name, school_name, grade_class, contact_info) VALUES (?, ?, ?, ?)",
                   ("Jay", "MCC", "10-A", "0912"))
    student_id = cursor.lastrowid

    today = date.today().isoformat()
    due = (date.today() + timedelta(days=7)).isoformat()

    cursor.executemany("""
        INSERT INTO loans (book_id, student_id, borrow_date, due_date, status)
        VALUES (?, ?, ?, ?, 'BORROWED')
    """, [
        (1, student_id, today, due),
        (1, student_id, today, due),
        (2, student_id, today, due)
    ])

    conn.commit()
    conn.close()

    library_service.report_most_borrowed_books()
    output = capsys.readouterr().out

    assert "Most Borrowed Books" in output
    assert "Book A" in output
    assert "Book B" in output
    assert output.index("Book A") < output.index("Book B")


def test_report_total_books_per_school(test_db, capsys):
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO books (isbn, title, author, genre, quantity) VALUES (?, ?, ?, ?, ?)",
                   ("X1", "Math Book", "Teacher A", "Education", 3))
    cursor.execute("INSERT INTO books (isbn, title, author, genre, quantity) VALUES (?, ?, ?, ?, ?)",
                   ("X2", "Science Book", "Teacher B", "Education", 3))

    cursor.execute("INSERT INTO students (name, school_name, grade_class, contact_info) VALUES (?, ?, ?, ?)",
                   ("Ana", "School A", "10-A", "0901"))
    s1 = cursor.lastrowid

    cursor.execute("INSERT INTO students (name, school_name, grade_class, contact_info) VALUES (?, ?, ?, ?)",
                   ("Ben", "School B", "10-B", "0902"))
    s2 = cursor.lastrowid

    today = date.today().isoformat()
    due = (date.today() + timedelta(days=7)).isoformat()

    cursor.executemany("""
        INSERT INTO loans (book_id, student_id, borrow_date, due_date, status)
        VALUES (?, ?, ?, ?, 'BORROWED')
    """, [
        (1, s1, today, due), 
        (2, s2, today, due),
        (2, s2, today, due)  
    ])

    conn.commit()
    conn.close()

    library_service.report_total_books_per_school()
    output = capsys.readouterr().out

    assert "Total Borrowed Books Per School" in output
    assert "School B" in output
    assert "School A" in output
    assert output.index("School B") < output.index("School A") 


def test_view_student_history_no_history(test_db, capsys):
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students (name, school_name, grade_class, contact_info)
        VALUES (?, ?, ?, ?)
    """, ("Mia", "MCC", "12-A", "0910"))
    student_id = cursor.lastrowid

    conn.commit()
    conn.close()

    library_service.view_student_history(student_id)
    output = capsys.readouterr().out

    assert "No loan history" in output


def test_view_student_history_with_data(test_db, capsys):
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO books (isbn, title, author, genre, quantity) VALUES (?, ?, ?, ?, ?)",
                   ("HX1", "History Book", "Prof A", "History", 2))
    book_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO students (name, school_name, grade_class, contact_info)
        VALUES (?, ?, ?, ?)
    """, ("Leo", "MCC", "11-B", "0913"))
    student_id = cursor.lastrowid

    today = date.today().isoformat()
    due = (date.today() + timedelta(days=5)).isoformat()

    cursor.execute("""
        INSERT INTO loans (book_id, student_id, borrow_date, due_date, status)
        VALUES (?, ?, ?, ?, 'BORROWED')
    """, (book_id, student_id, today, due))

    conn.commit()
    conn.close()

    library_service.view_student_history(student_id)
    output = capsys.readouterr().out

    assert "Loan ID" in output
    assert "HX1" in output
    assert "BORROWED" in output
    assert today in output