import sqlite3
from datetime import datetime, timedelta
from src.database import create_connection

# TODO: Finish Placeholder Methods

def add_book(isbn, title, author, genre, quantity):
    # Adds a new book to the database.
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

def register_student(name, school_name, grade_class, contact_info):
    # Registers a new student.
    # Logic to insert student goes here
    print("Feature not implemented yet.")

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