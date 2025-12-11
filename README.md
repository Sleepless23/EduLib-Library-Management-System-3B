# EduLib - Library Management System

A centralized digital library system for the EduLib Schools Consortium. This system replaces Excel/paper records to manage books, students, and loans across 14 schools.

## 🚀 Getting Started

### Prerequisites
*   Python 3.8+
*   Git

### Installation & Setup

1.  **Clone the branch:**
    ```bash
    git clone -b development https://github.com/Sleepless23/EduLib-Library-Management-System-3B.git
    cd edulib-system
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate
      Notes from Bon: Download requests by (pip install requests) command and be sure you are inside your virtual environment(venv)
      https://books.google.com/  (You can find the list of books and their ISBN here)
    ```

3.  **Run the Application:**
    This will initialize the SQLite database automatically on the first run.
    ```bash
    python -m src.main
    ```

---



## 🛠️ Development Workflow

We follow a feature-branch workflow. **Do not push directly to `main` or `development`.**

1.  Checkout the development branch: `git checkout development`
2.  Pull latest changes: `git pull origin development`
3.  Create your feature branch: `git checkout -b feature/your-feature-name`
4.  Commit your changes.
5.  Push and open a Pull Request (PR) to `development`.

This is to ensure quality control and prevent accidental pushing of buggy code to the main/dev branch.

---

## 📜 Project Architecture:
The file structure of the project, when finished, should look something like this:

```
edulib-system/
│
├── docs/                  # SDLC & Waterfall documentation
├── src/                   # Source Code
│   ├── database.py        # SQL connections & table creation
│   ├── models.py          # Data classes (Book, Student)
│   ├── library_service.py # Logic (Borrow, Return, Add logic)
│   ├── main.py            # The Menu / User Interface
│   └── __init__.py        # Makes 'src' a package
│
├── tests/                 # Unit tests
├── .gitignore             # Git ignore file
├── README.md              # Project documentation
└── requirements.txt       # Dependencies
```

---

## ✅ Project Task List (TODO)

Please check off items as you complete them by updating this README in your PR (Pull Request).

### Phase 1: Core Database & Models
- [x] Setup Project Structure
- [x] Implement SQLite Connection (`src/database.py`)
- [x] Define Database Schema (Books, Students, Loans tables)
- **NOTE: The 'edulib.db' file is included in .gitignore to ensure local data does not get uploaded to GitHub. You will generate your own 'edulib.db' when you run the code**

### Phase 2: Book Management (`src/library_service.py`)
- [x] Add Book Function
- [x] Edit Book Details Function
- [x] Delete Book Function
- [x] **Optional:** Google Books API integration to auto-fill details by ISBN

### Phase 3: Student Management
- [x] Register Student (Name, Class, School, Contact)
- [x] Edit Student Details
- [x] View Student History

### Phase 4: Borrowing System
- [x] Check availability before borrowing
- [x] **Borrow Book Function:** Record loan, set due date (auto 14 days), decrement quantity
- [ ] **Return Book Function:** Update status, increment quantity
- [ ] Prevent borrowing if student has overdue books

### Phase 5: Reporting
- [ ] Report: Most Borrowed Books
- [ ] Report: Overdue Books List
- [ ] Report: Total Books per School
- [ ] Export reports to CSV/PDF

### Phase 6: Testing & UI
- [ ] Write Unit Tests (`tests/`)
- [ ] Update CLI Menu in `src/main.py` to connect all functions
- [ ] Final User Testing
