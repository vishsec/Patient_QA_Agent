from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def render_labs_pdf(patient, out_path: str | Path) -> None:
    """Render a patient's lab results as a deterministic 4-column PDF table."""
    # Ensure the parent directory exists before writing
    out_file = Path(out_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    

    sex_code = str(patient.sex).strip().upper()[0]
    # 1. Header Paragraph (e.g., "Patient P001 — 60M — Labs")
    # Adjust attribute names (patient.id, patient.age, patient.sex) to match your dataclass
    header_text = f"Patient {patient.id} — {patient.age}{sex_code} — Labs"
    title = Paragraph(header_text, styles["Heading2"])

    # 1. Build the 2D grid matching the exact header order: Analyte, Value, Unit, Week
    data = [["Analyte", "Value", "Unit", "Week"]]
    for lab in patient.labs:
        data.append([
            str(lab.analyte),
            str(lab.value),
            str(lab.unit),
            str(lab.week),
        ])

    # 2. Define the table with explicit column widths (72 points = 1 inch)
    # Total width = 468pt (fits comfortably inside standard letter margins)
    col_widths = [180, 96, 108, 84]
    table = Table(data, colWidths=col_widths)

    # 3. Apply clean styling for readability and reliable pdfplumber extraction
    style = TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 1), (1, -1), "RIGHT"),   # Right-align numeric values
        ("ALIGN", (3, 0), (3, -1), "CENTER"),  # Center-align week numbers
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ])
    table.setStyle(style)

    # 4. Build the PDF deterministically using the caller-provided path
    doc = SimpleDocTemplate(str(out_file), pagesize=letter)
    doc.build([title, Spacer(1,12), table])


if __name__ == "__main__":
    from corpus.patients import P001

    render_labs_pdf(P001, "data/raw/P001/labs.pdf")
    print("Generated data/raw/P001/labs.pdf successfully.")
