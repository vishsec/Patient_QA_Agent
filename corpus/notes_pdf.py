from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def render_notes_pdf(patient , out_path: str | Path) -> None:
    styles = getSampleStyleSheet()
    sex_code = str(patient.sex).strip().upper()[0]
    story = [Paragraph(f"Patient {patient.id} - {patient.age}{sex_code} - Clinical Notes", styles["Heading2"])]
    for n in patient.notes:
        story.append(Paragraph(f"Notes for the week {n.week}", styles["Heading3"])) # weekly because chunks  can eb leballed weekly and answerered accordingly 
        story.append(Paragraph(n.text, styles["BodyText"]))
    SimpleDocTemplate(str(out_path), pagesize=letter).build(story)

if __name__ == "__main__":
    from corpus.patients import P001
    render_notes_pdf(P001, "data/raw/P001/notes.pdf")
    print("Generated data/raw/P001/notes.pdf successfully")



