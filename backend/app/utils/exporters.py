import csv
from datetime import date
from io import StringIO, BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from app.models import Expense

def generate_csv(expenses: list[Expense], user_name: str) -> str:
    output = StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow(['Titre', 'Montant (DH)', 'Date', 'Catégorie', 'Note'])

    # Données
    for expense in expenses:
        writer.writerow([
            expense.title,
            str(expense.amount),
            expense.date.isoformat(),
            expense.category.name if expense.category else '',
            expense.note or ''
        ])

    # Footer avec totaux
    total = sum(e.amount for e in expenses)
    writer.writerow(['', '', '', 'TOTAL', str(total)])

    return output.getvalue()

def generate_pdf(expenses: list[Expense], user_name: str, start_date: date = None, end_date: date = None) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1A1917'),
        spaceAfter=12,
        alignment=1  # Center
    )

    story = []

    # Titre
    title = Paragraph(f"Rapport d'Dépenses - {user_name}", title_style)
    story.append(title)

    # Dates
    if start_date and end_date:
        date_range = Paragraph(f"Période : {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}", styles['Normal'])
    else:
        date_range = Paragraph(f"Généré le {date.today().strftime('%d/%m/%Y')}", styles['Normal'])
    story.append(date_range)
    story.append(Spacer(1, 12))

    # Tableau
    data = [['Titre', 'Montant (DH)', 'Date', 'Catégorie', 'Note']]
    for expense in expenses:
        data.append([
            expense.title,
            f"{float(expense.amount):.2f}",
            expense.date.strftime('%d/%m/%Y'),
            expense.category.name if expense.category else '-',
            expense.note or '-'
        ])

    # Total
    total = sum(e.amount for e in expenses)
    data.append(['', '', '', 'TOTAL', f"{float(total):.2f}"])

    table = Table(data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1D4ED8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F0EEE9')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#F7F6F3')]),
    ]))

    story.append(table)

    # Build
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
