from src.database import initialize_db, create_connection
from src.library_service import add_book, add_book_with_isbn, edit_book, remove_book
from src.library_service import register_student, edit_student, show_students

def print_menu():
    print("\n--- EduLib Library System ---")
    print("1. Add New Book")
    print("2. Register, Edit and Show Student")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Generate Reports")
    print("6. Edit Book Details")
    print("7. Delete Book")
    print("8. Exit")

def main():
    initialize_db()

    while True:
        print_menu()
        choice = input("Select an option (1-8): ").strip()

        # Add Book choice
        if choice == '1':
            isbn = input("Enter ISBN (leave blank to enter manually): ").strip()
            if isbn:
                qty_input = input("Enter Quantity: ").strip()
                qty = int(qty_input) if qty_input else 1
                add_book_with_isbn(isbn, qty)
            else:
                title = input("Enter Title: ").strip()
                author = input("Enter Author: ").strip()
                genre = input("Enter Genre: ").strip()
                qty_input = input("Enter Quantity: ").strip()
                qty = int(qty_input) if qty_input else 1
                isbn_manual = input("Enter ISBN: ").strip()
                add_book(isbn_manual, title, author, genre, qty)

        # Register Student choice
        elif choice == '2':
            while True:
                print("\n=== Student Management ===")
                print("1. Register Student")
                print("2. Edit Student Details")
                print("3. Show all students")
                print("0. Back to Main Menu")
                stu_choice = input("Enter your choice: ").strip()

                if stu_choice == "1":
                    name = input("Enter student name: ").strip()
                    grade_class = input("Enter student class/section: ").strip()
                    school = input("Enter student school: ").strip()
                    contact = input("Enter contact number: ").strip()
                    register_student(name, school, grade_class, contact)

                elif stu_choice == "2":
                    try:
                        student_id = int(input("Enter Student ID to edit: ").strip())
                    except ValueError:
                        print("Invalid input! Must be a number.")
                        continue

                    name = input("Enter new name (leave blank to keep current): ").strip() or None
                    grade_class = input("Enter new class (leave blank to keep current): ").strip() or None
                    school = input("Enter new school (leave blank to keep current): ").strip() or None
                    contact = input("Enter new contact (leave blank to keep current): ").strip() or None
                    edit_student(student_id, name, school, grade_class, contact)

                elif stu_choice == "3":
                    show_students()
                elif stu_choice == "0":
                    break
                else:
                    print("Invalid choice, try again.")

        # Borrow Book choice
        elif choice == '3':
            print("Feature currently under development.")

        # Return Book choice
        elif choice == '4':
            print("Feature currently under development.")

        # Generate report
        elif choice == '5':
            print("Feature currently under development.")

        # Edit Book choice
        elif choice == '6':
            isbn = input("Enter ISBN of book to edit: ").strip()

            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, title, author, genre, quantity FROM books WHERE isbn = ?",
                (isbn,)
            )
            result = cursor.fetchone()
            conn.close()

            if result is None:
                print("Book not found.")
            else:
                book_id, old_title, old_author, old_genre, old_qty = result

                print(f"Current Title: {old_title}, Author: {old_author}, Genre: {old_genre}, Quantity: {old_qty}")

                title = input("New Title (leave blank to keep current): ").strip() or old_title
                author = input("New Author (leave blank to keep current): ").strip() or old_author
                genre = input("New Genre (leave blank to keep current): ").strip() or old_genre
                qty_input = input("New Quantity (leave blank to keep current): ").strip()
                qty = int(qty_input) if qty_input else old_qty

                edit_book(book_id, title, author, genre, qty)
                print("Book updated successfully.")

        # Delete Book choice
        elif choice == '7':
            isbn = input("Enter ISBN of book to delete: ").strip()

            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, title FROM books WHERE isbn = ?", (isbn,))
            result = cursor.fetchone()
            conn.close()

            if result is None:
                print("Book not found.")
            else:
                book_id, title = result
                confirm = input(f"Are you sure you want to delete '{title}'? (Y/N): ").upper()
                if confirm == "Y":
                    remove_book(book_id)
                    print("Book deleted successfully.")
                else:
                    print("Deletion cancelled.")

        # Exit choice
        elif choice == '8':
            print("Exiting system. Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
