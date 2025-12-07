import sqlite3
from sqlite3 import Error

DB_FILE = "edulib.db"

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def initialize_db():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # 1. Books Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    isbn TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    genre TEXT,
                    quantity INTEGER DEFAULT 1
                );
            """)

            # 2. Students Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    school_name TEXT NOT NULL,
                    grade_class TEXT,
                    contact_info TEXT
                );
            """)

            # 3. Loans Table (Tracks borrowing)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS loans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER,
                    student_id INTEGER,
                    borrow_date DATE NOT NULL,
                    due_date DATE NOT NULL,
                    return_date DATE,
                    status TEXT DEFAULT 'BORROWED',
                    FOREIGN KEY (book_id) REFERENCES books (id),
                    FOREIGN KEY (student_id) REFERENCES students (id)
                );
            """)
            
            conn.commit()
            print("Database initialized successfully.")
        except Error as e:
            print(f"Database initialization error: {e}")
        finally:
            conn.close()
    else:
        print("Error! Cannot create the database connection.")

def update_book(book_id, title, author, genre, quantity):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE books
        SET title = ?, author = ?, genre = ?, quantity = ?
        WHERE id = ?
    """, (title, author, genre, quantity, book_id))
    conn.commit()
    conn.close()


def delete_book(book_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
