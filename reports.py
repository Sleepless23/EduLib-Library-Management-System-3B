from datetime import datetime, date
import csv
import sqlite3

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from database import get_connection


def fetch_overdue_loans(as_of_date=None):
    """Fetch overdue books where due_date < today and not returned."""
    conn = get_connection()

    if as_of_date is None:
        as_of_date = date.today().isoformat()
    elif isinstance(as_of_date, date):
        as_of_date = as_of_date.isoformat()

    sql = """
    SELECT loans.id AS loan_id,
           books.id AS book_id,
           books.title,
           books.isbn,
           students.id AS student_id,
           students.full_name,
           students.class,
           students.school,
           loans.borrow_date,
           loans.due_date
    FROM loans
    JOIN books ON loans.book_id = books.id
    JOIN students ON loans.student_id = students.id
    WHERE loans.return_date IS NULL
      AND DATE(loans.due_date) < DATE(?)
    ORDER BY DATE(loans.due_date) ASC;
    """

    cur = conn.execute(sql, (as_of_date,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def export_overdue_to_csv(rows, filename):
    """Write overdue loans to a CSV file."""
    if not rows:
        headers = ["loan_id", "book_id", "title", "isbn", "student_id",
                   "full_name", "class", "school", "borrow_date", "due_date"]
    else:
        headers = rows[0].keys()

    with open(filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    return filename


def export_overdue_to_pdf(rows, filename):
    """Generate a simple PDF report using ReportLab."""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("Overdue Books Report", styles["Title"]))
    elements.append(
        Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                  styles["Normal"])
    )
    elements.append(Spacer(1, 12))

    data = [
        ["Loan ID", "Book", "ISBN", "Student", "Class", "School",
         "Borrowed", "Due", "Days Overdue"]
    ]

    today = date.today()

    for row in rows:
        due = datetime.strptime(row["due_date"], "%Y-%m-%d").date()
        days_over = (today - due).days

        data.append([
            str(row["loan_id"]),
            row["title"],
            row["isbn"] or "",
            row["full_name"],
            row["class"] or "",
            row["school"] or "",
            row["borrow_date"],
            row["due_date"],
            str(days_over)
        ])

    table = Table(data, repeatRows=1)
    table_style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.gray),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ])
    table.setStyle(table_style)

    elements.append(table)
    doc.build(elements)

    return filename


def generate_overdue_reports(csv_file="overdue_report.csv", pdf_file="overdue_report.pdf"):
    """Fetch overdue loans and export both CSV & PDF."""
    rows = fetch_overdue_loans()
    export_overdue_to_csv(rows, csv_file)
    export_overdue_to_pdf(rows, pdf_file)
    return csv_file, pdf_file
