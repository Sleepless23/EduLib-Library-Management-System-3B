from reports import generate_overdue_reports

def add_book():
    print("Add Book function not yet implemented.")

def edit_book():
    print("Edit Book function not yet implemented.")

def delete_book():
    print("Delete Book function not yet implemented.")

def register_student():
    print("Register Student function not yet implemented.")

def edit_student():
    print("Edit Student function not yet implemented.")

def borrow_book():
    print("Borrow Book function not yet implemented.")

def return_book():
    print("Return Book function not yet implemented.")

def view_student_history():
    print("View Student History function not yet implemented.")

def most_borrowed_books():
    print("Most Borrowed Books report not yet implemented.")

def total_books_per_school():
    print("Total Books per School report not yet implemented.")

def generate_overdue_menu():
    print("\n--- OVERDUE BOOKS REPORT ---")
    csv_name = input("CSV filename (default: overdue.csv): ").strip() or "overdue.csv"
    pdf_name = input("PDF filename (default: overdue.pdf): ").strip() or "overdue.pdf"
    csv_file, pdf_file = generate_overdue_reports(csv_name, pdf_name)
    print("\nReports generated successfully:")
    print(f" - CSV: {csv_file}")
    print(f" - PDF: {pdf_file}\n")

def main_menu():
    while True:
        print("\n======================================")
        print("      EDU-LIB LIBRARY SYSTEM")
        print("======================================")
        print("1) Add Book")
        print("2) Edit Book")
        print("3) Delete Book")
        print("4) Register Student")
        print("5) Edit Student")
        print("6) Borrow Book")
        print("7) Return Book")
        print("8) View Student History")
        print("9) Most Borrowed Books Report")
        print("10) Total Books Per School Report")
        print("11) Overdue Books Report (CSV + PDF)")
        print("0) Exit")
        print("======================================")

        choice = input("Select an option: ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            edit_book()
        elif choice == "3":
            delete_book()
        elif choice == "4":
            register_student()
        elif choice == "5":
            edit_student()
        elif choice == "6":
            borrow_book()
        elif choice == "7":
            return_book()
        elif choice == "8":
            view_student_history()
        elif choice == "9":
            most_borrowed_books()
        elif choice == "10":
            total_books_per_school()
        elif choice == "11":
            generate_overdue_menu()
        elif choice == "0":
            print("Exiting system... Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()
