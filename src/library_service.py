import sqlite3
from src.database import create_connection, update_book, delete_book
import requests

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
    """
    Logic:
    1. Check if book quantity > 0.
    2. Check if student exists.
    3. Insert into loans table with due_date (today + 14 days).
    4. Decrement book quantity in books table.
    """
    print("Feature not implemented yet.")

def return_book(loan_id):
    """
    Logic:
    1. Update loan status to 'RETURNED'.
    2. Set return_date to today.
    3. Increment book quantity in books table.
    """
    print("Feature not implemented yet.")

def generate_report_books_per_school():
    # Generates a report of books distribution.
    print("Feature not implemented yet.")