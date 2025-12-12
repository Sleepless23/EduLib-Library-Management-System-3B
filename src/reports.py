import csv
import sqlite3
from datetime import datetime, date
from src.database import create_connection

# ReportLab imports for PDF generation
# Run: pip install reportlab
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

def fetch_overdue_loans():
    """Fetch overdue books where due_date < today and status is BORROWED."""
    conn = create_connection()
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    cursor = conn.cursor()

    today_iso = date.today().isoformat()

    # Query matches your database.py schema
    sql = """
    SELECT l.id AS loan_id,
           b.title,
           b.isbn,
           s.name AS student_name,
           s.grade_class,
           s.school_name,
           l.borrow_date,
           l.due_date
    FROM loans l
    JOIN books b ON l.book_id = b.id
    JOIN students s ON l.student_id = s.id
    WHERE l.status = 'BORROWED'
      AND l.due_date < ?
    ORDER BY l.due_date ASC;
    """

    cursor.execute(sql, (today_iso,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def export_overdue_to_csv(rows, filename):
    """Write overdue loans to a CSV file."""
    if not rows:
        return None

    headers = rows[0].keys()

    try:
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        return filename
    except IOError as e:
        print(f"Error writing CSV: {e}")
        return None

def export_overdue_to_pdf(rows, filename):
    """Generate a simple PDF report using ReportLab."""
    if not PDF_AVAILABLE:
        print("Error: 'reportlab' module not found. Please run: pip install reportlab")
        return None

    if not rows:
        return None

    try:
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Title
        elements.append(Paragraph("Overdue Books Report", styles["Title"]))
        elements.append(
            Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                      styles["Normal"])
        )
        elements.append(Spacer(1, 12))

        # Table Headers
        table_data = [
            ["Loan ID", "Book", "Student", "Class", "Due Date", "Days Late"]
        ]

        today = date.today()

        # Table Rows
        for row in rows:
            try:
                due = datetime.strptime(row["due_date"], "%Y-%m-%d").date()
                days_over = (today - due).days
            except ValueError:
                days_over = "?"

            table_data.append([
                str(row["loan_id"]),
                row["title"][:20], # Truncate long titles
                row["student_name"],
                row["grade_class"] or "",
                row["due_date"],
                str(days_over)
            ])

        # Table Styling
        table = Table(table_data)
        table_style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.gray),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
        ])
        table.setStyle(table_style)

        elements.append(table)
        doc.build(elements)
        return filename
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None

def generate_overdue_reports(csv_filename="overdue.csv", pdf_filename="overdue.pdf"):
    """Fetch overdue loans and export both CSV & PDF."""
    print("Fetching overdue data...")
    rows = fetch_overdue_loans()
    
    if not rows:
        print("No overdue books found! Skipping report generation.")
        return

    print(f"Found {len(rows)} overdue items.")
    
    csv_res = export_overdue_to_csv(rows, csv_filename)
    if csv_res:
        print(f" -> CSV generated: {csv_res}")

    pdf_res = export_overdue_to_pdf(rows, pdf_filename)
    if pdf_res:
        print(f" -> PDF generated: {pdf_res}")