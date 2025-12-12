import sqlite3
from src.database import create_connection, update_book, delete_book
import requests
from datetime import date, timedelta

# Existing Add Book
def add_book(isbn, title, author, genre, quantity):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO books (isbn, title, author, genre, quantity) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(sql, (isbn, title, author, genre, quantity))
        conn.commit()
        print(f"Success: Book '{title}' added.")
    except sqlite3.IntegrityError:
        print("Error: A book with this ISBN already exists.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# Google Books API
def fetch_book_by_isbn(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(url).json()
    if "items" not in response:
        return None
    info = response["items"][0]["volumeInfo"]
    return {
        "title": info.get("title", ""),
        "author": ", ".join(info.get("authors", ["Unknown"])),
        "genre": info.get("categories", ["General"])[0]
    }

# Add Book with ISBN Lookup
def add_book_with_isbn(isbn, quantity=1):
    book_data = fetch_book_by_isbn(isbn)
    if book_data is None:
        print("Book not found in Google Books API.")
        return

    conn = create_connection()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO books (isbn, title, author, genre, quantity) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(sql, (isbn, book_data['title'], book_data['author'], book_data['genre'], quantity))
        conn.commit()
        print(f"Success: Book '{book_data['title']}' added via ISBN lookup.")
    except sqlite3.IntegrityError:
        print("Error: A book with this ISBN already exists.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# Edit Book
def edit_book(book_id, title, author, genre, quantity):
    update_book(book_id, title, author, genre, quantity)

# Delete Book
def remove_book(book_id):
    delete_book(book_id)


def register_student(name, school_name, grade_class, contact_info):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO students (name, school_name, grade_class, contact_info)
        VALUES (?, ?, ?, ?)
    """, (name, school_name, grade_class, contact_info))
    conn.commit()
    conn.close()
    print(f"Student {name} registered successfully.")

# Edit Student
def edit_student(student_id, name=None, school_name=None, grade_class=None, contact_info=None):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    if not student:
        print("Student not found!")
        conn.close()
        return

    # Keep old values if new ones not provided
    name = name or student[1]
    school_name = school_name or student[2]
    grade_class = grade_class or student[3]
    contact_info = contact_info or student[4]

    cursor.execute("""
        UPDATE students
        SET name = ?, school_name = ?, grade_class = ?, contact_info = ?
        WHERE id = ?
    """, (name, school_name, grade_class, contact_info, student_id))
    conn.commit()
    conn.close()
    print(f"Student ID {student_id} updated successfully.")

# Show all Students
def show_students():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, grade_class, school_name, contact_info FROM students")
    students = cursor.fetchall()
    conn.close()

    if not students:
        print("No students registered yet.")
        return

    print("=== All Students ===")
    for s in students:
        print(f"ID: {s[0]} | Name: {s[1]} | Class: {s[2]} | School: {s[3]} | Contact: {s[4]}")

def borrow_book(book_isbn, student_id):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # 1. Check student
        cursor.execute("SELECT id FROM students WHERE id = ?", (student_id,))
        if cursor.fetchone() is None:
            print("Error: Student not found.")
            return

        # 2. Check book
        cursor.execute(
            "SELECT id, title, quantity FROM books WHERE isbn = ?",
            (book_isbn,)
        )
        book = cursor.fetchone()
        if book is None:
            print("Error: Book not found.")
            return

        book_id, title, quantity = book

        if quantity < 1:
            print(f"Sorry, '{title}' is unavailable.")
            return

        # 3. Create loan (today + 14 days)
        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=14)

        cursor.execute("""
            INSERT INTO loans (book_id, student_id, borrow_date, due_date, status)
            VALUES (?, ?, ?, ?, 'BORROWED')
        """, (book_id, student_id, borrow_date.isoformat(), due_date.isoformat()))

        # 4. Update book quantity
        cursor.execute(
            "UPDATE books SET quantity = quantity - 1 WHERE id = ?",
            (book_id,)
        )

        conn.commit()
        print(f"Success: '{title}' borrowed! Due on {due_date}.")

    except sqlite3.Error as e:
        conn.rollback()
        print("Database error:", e)

    finally:
        conn.close()

def return_book(loan_id):
    """
    Logic:
    1. Update loan status to 'RETURNED'.
    2. Set return_date to today.
    3. Increment book quantity in books table.
    """
    print("Feature not implemented yet.")

def view_student_history(student_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        sql = """
        SELECT loan_id, book_isbn, loan_date, due_date, return_date, status
        FROM loans
        WHERE student_id = ?
        ORDER BY loan_date DESC
        """
        cursor.execute(sql, (student_id,))
        rows = cursor.fetchall()

        if not rows:
            print("No loan history for this student.")
            return

        print(f"{'Loan ID':<8} {'ISBN':<15} {'Loan Date':<12} {'Due Date':<12} {'Return Date':<12} {'Status'}")
        print("-" * 70)

        for loan_id, isbn, loan_date, due_date, return_date, status in rows:
            print(f"{loan_id:<8} {isbn:<15} {loan_date:<12} {due_date:<12} {str(return_date):<12} {status}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn.close()

def report_most_borrowed_books():
    conn = create_connection()
    cursor = conn.cursor()

    sql = """
    SELECT b.title, b.author, COUNT(l.id) AS borrow_count
    FROM loans l
    JOIN books b ON l.book_id = b.id
    GROUP BY b.id
    HAVING borrow_count > 0
    ORDER BY borrow_count DESC
    LIMIT 10;
    """

    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("\nNo borrowing data available yet.")
        return

    print("\n=== Most Borrowed Books ===")
    print(f"{'Title':<40} {'Author':<25} {'Times Borrowed'}")
    print("-" * 80)

    for title, author, count in rows:
        print(f"{title:<40} {author:<25} {count}")

def report_total_books_per_school():
    conn = create_connection()
    cursor = conn.cursor()

    sql = """
    SELECT s.school_name, COUNT(l.id) AS total_borrowed
    FROM loans l
    JOIN students s ON l.student_id = s.id
    GROUP BY s.school_name
    HAVING total_borrowed > 0
    ORDER BY total_borrowed DESC;
    """

    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("\nNo borrowing activity yet.")
        return

    print("\n=== Total Borrowed Books Per School ===")
    print(f"{'School':<40} {'Books Borrowed'}")
    print("-" * 60)

    for school, total in rows:
        print(f"{school:<40} {total}")
