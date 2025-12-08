students = []

#reg student
def register_student():
    print("=== Register Student ===")
    name = input("Enter student name: ")
    class_name = input("Enter student class/section: ")
    school = input("Enter student school: ")
    contact = input("Enter contact number: ")

    student = {
        "id": len(students) + 1,
        "name": name,
        "class": class_name,
        "school": school,
        "contact": contact
    }

    students.append(student)
    print(f"Student {name} has been registered successfully!")

#edit student
def edit_student():
    print("=== Edit Student Details ===")
    
    if not students:
        print("No students registered yet.")
        return

    print("Current students:")
    for s in students:
        print(f"ID: {s['id']} | Name: {s['name']} | Class: {s['class']} | School: {s['school']}")

    try:
        student_id = int(input("Enter student ID to edit: "))
    except ValueError:
        print("Invalid input! Please enter a number.")
        return

    student = None
    for s in students:
        if s["id"] == student_id:
            student = s
            break

    if student is None:
        print("Student not found!")
        return

    print("Press Enter to keep the current value.")
    name = input(f"Enter new name ({student['name']}): ") or student['name']
    class_name = input(f"Enter new class ({student['class']}): ") or student['class']
    school = input(f"Enter new school ({student['school']}): ") or student['school']
    contact = input(f"Enter new contact ({student['contact']}): ") or student['contact']

    student["name"] = name
    student["class"] = class_name
    student["school"] = school
    student["contact"] = contact

    print(f"Student ID {student_id} has been updated successfully!")

#show all students
def show_students():
    if not students:
        print("No students registered yet.")
        return
    print("=== All Students ===")
    for s in students:
        print(f"ID: {s['id']} | Name: {s['name']} | Class: {s['class']} | School: {s['school']} | Contact: {s['contact']}")

def main_menu():
    while True:
        print("\n=== Student Management ===")
        print("1. Register Student")
        print("2. Edit Student Details")
        print("3. Show all students")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_student()
        elif choice == "2":
            edit_student()
        elif choice == "3":
            show_students()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main_menu()
