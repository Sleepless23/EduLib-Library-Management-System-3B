## 📚 SDLC Documentation: EduLib Library System
**Methodology:** Waterfall Model\
**Project:** EduLib Schools Consortium - Library Management System\
**Members:** Princes Ann Bautista, Richard Bengco, John Terrelle
Cabillon, Charles David, Vince Russel Garcia, Brix Andrew Ibuna,
Alyannce Vaughn Laxamana, Sean Masa, Janrey Nicdao, Markedrei Sangalang

---
## 1. Introduction

The **EduLib Library Management System** is a centralized software
solution designed to replace legacy methods (Excel spreadsheets and
paper records) for the EduLib Schools Consortium. The system manages the
library inventory, student registry, and circulation (loans/returns)
across 14 schools.

We have adopted the **Waterfall Model** for this project. This linear,
sequential approach was chosen because the requirements were clearly
defined by the consortium upfront, and the system requires a stable
database architecture before application logic could be built.

## 2. Phases of Development

### Phase 1: Requirement Gathering & Analysis

In this initial phase, we defined the specific needs of the library
administrators and the constraints of the system.

**Functional Requirements:**

-   **Inventory Management:** Ability to Add, Edit, and Delete books.
    Integration with **Google Books API** to fetch book details via ISBN
    automatically.

-   **Student Management:** Register and edit student details (Name,
    School, Grade, Contact). View loan history per student.

-   **Circulation:**

    -   Borrow books with an automatic 14-day due date.

    -   Prevent borrowing if the book quantity is 0.

    -   **Logic Rule:** Prevent borrowing if the student currently has
        overdue books.

    -   Return books and update inventory counts immediately.

-   **Reporting:**

    -   Generate reports for \"Most Borrowed Books\" and \"Total Books
        per School.\"

    -   Generate an \"Overdue Books\" report exportable to **CSV** and
        **PDF**.

**Non-Functional Requirements:**

-   **Platform:** Python 3.8+ (Command Line Interface).

-   **Database:** SQLite (Local storage, zero-configuration).

-   **Portability:** Must run in a virtual environment with minimal
    dependencies (requests, reportlab).
---
### Phase 2: System Design

Before writing code, the system architecture and database schema were
designed to ensure data integrity.

**2.1 Database Schema (ERD Concept)**

-   **Books Table:** Stores id, isbn (Unique), title, author, genre,
    quantity.

-   **Students Table:** Stores id, name, school_name, grade_class,
    contact_info.

-   **Loans Table:** Linking entity containing id, book_id (FK),
    student_id (FK), borrow_date, due_date, return_date, status.

**2.2 Modular Architecture**

The system is designed with a separation of concerns:

-   database.py: Handles raw SQL connections and table initialization.

-   library_service.py: Contains the business logic (calculations, API
    calls, constraints).

-   reports.py: Dedicated module for file generation (PDF/CSV).

-   main.py: The presentation layer (CLI Menu) handling user input.
---
### Phase 3: Implementation

This phase involved the actual coding of the system, following the
sequence defined in the architecture.

**Step 1: Core Foundation**

-   Established src/database.py to create the SQLite database
    (edulib.db) and tables automatically on startup.

**Step 2: Business Logic**

-   Implemented CRUD operations in src/library_service.py.

-   Integrated the **Google Books API** using the requests library to
    enhance the \"Add Book\" feature.

-   Implemented the logic for the 14-day loan period using Python\'s
    datetime and timedelta.

**Step 3: Advanced Logic & Reporting**

-   Implemented src/reports.py using reportlab for PDF generation and
    the native csv library for data export.

-   Added the \"Overdue Check\" logic to the borrowing function to
    enforce library rules.

**Step 4: User Interface**

-   Built the Command Line Interface (CLI) in src/main.py to tie all
    functions together into a navigational menu.

**Dev Workflow:** utilized a **Feature-Branch workflow** (Git) where
developers merged code into a development branch before finalizing.
---
### Phase 4: Testing

Testing was conducted to ensure all requirements from Phase 1 were met.

**4.1 Unit Testing**

-   Automated tests located in tests/ to verify:

    -   Database connection reliability.

    -   Book quantity decrementing upon borrowing.

    -   Book quantity incrementing upon return.

**4.2 System & Integration Testing**

-   **API Test:** Verified that entering an ISBN fetches the correct
    Title/Author from Google.

-   **Constraint Test:** Attempted to borrow a book for a student with
    an overdue item (Expected Result: System blocks transaction).

-   **Report Test:** Generated PDF/CSV files to ensure formatting is
    correct and files are readable.
---
### Phase 5: Deployment

The system is deployed locally to the school administrators\' machines.

**Deployment Checklist:**

1.  **Environment Setup:** Python 3.8+ installed.

2.  **Dependencies:** Execution of pip install requests reportlab.

3.  **Initialization:** First run of python -m src.main initializes the
    local edulib.db file.

4.  **Security:** The .gitignore file ensures that the local database
    containing student data is never uploaded to the public code
    repository.
---
### Phase 6: Maintenance

The final phase of the Waterfall model, occurring after the system is in
use.

-   **Bug Fixes:** Addressing any runtime errors reported by librarians.

-   **Data Backups:** Schools are advised to backup edulib.db weekly.

-   **Future Enhancements:** Potential plans to migrate from SQLite to
    PostgreSQL if the consortium grows beyond the current 14 schools.
