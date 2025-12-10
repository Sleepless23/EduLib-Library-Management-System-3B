from src.database import initialize_db
import src.library_service as service

def print_menu():
    print("\n--- EduLib Library System ---")
    print("1. Add New Book")
    print("2. Register Student")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Generate Reports")
    print("6. View Student History")
    print("7. Exit")

def main():
    initialize_db()

    while True:
        print_menu()
        choice = input("Select an option (1-7): ")

        if choice == '1':
            isbn = input("Enter ISBN: ")
            title = input("Enter Title: ")
            author = input("Enter Author: ")
            genre = input("Enter Genre: ")
            qty = int(input("Enter Quantity: "))
            service.add_book(isbn, title, author, genre, qty)
        
        elif choice == '2':
            # Example inputs
            # name = input("Student Name: ")
            # service.register_student(...)
            print("Feature currently under development.")

        elif choice == '3':
            print("Feature currently under development.")
            
        elif choice == '4':
            print("Feature currently under development.")

        elif choice == '5':
            print("Feature currently under development.")

        elif choice == '6':
            student_id = int(input("Enter Student ID: "))
            service.view_student_history(student_id)

        elif choice == '7':
            print("Exiting system. Goodbye!")
            break
        
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()