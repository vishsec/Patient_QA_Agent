# i need to be able to parse the pdf containing tables to extact facts. 
import pdfplumber
from corpus.patients import Labs, Meds, Note

def extract_lab_rows(pdf_path : str) -> list[Labs]:
    pdf = pdfplumber.open(pdf_path)
    tables = pdf.pages[0].extract_tables()
    table = tables[0] # since only one table
    #header row is table[0] ,values lies in body
    body =  table[1:]

    rows = []
    for row in body:
        rows.append(
            Labs(
                analyte=row[0].strip(),
                value=float(row[1].strip()),
                unit=row[2].strip(),
                week=int(row[3].strip()),
            )
        )
    return rows

def extract_med_rows(pdf_path : str) -> list[Meds]:
    pdf = pdfplumber.open(pdf_path)
    tables = pdf.pages[0].extract_tables()
    table = tables[0]

    body = table[1:]

    rows = []
    for row in body:
        rows.append(
            Meds(
                name = row[0].strip(),
                dose = row[1].strip(),
                frequency=row[2].strip(),
                week=int(row[3].strip()),
            )   
        ) 
    return rows

def extract_note_chunks(pdf_path : str) -> list[Note]:
    pdf = pdfplumber.open(pdf_path)
    text = pdf.pages[0].extract_text()

    notes=[]
    current_line = []
    current_week = None


    # remmeber the text files if needed

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        if line.startswith("Notes for the week"):
            if current_week is not None:
                notes.append(Note(week = current_week, text=" ".join(current_line)))
            current_week = int(line.split()[-1])
            current_line = []
        elif current_week is not None:
            current_line.append(line)

    if current_week is not None:
        notes.append(Note(week = current_week, text=" ".join(current_line)))

    return notes





if __name__ == "__main__":
    # result = extract_lab_rows("data/raw/P001/labs.pdf")
    # print(len(result))
    # print(result[0])

    result = extract_med_rows("data/raw/P001/meds.pdf")
    print(len(result))    # expect 3
    print(result[0])

    notes = extract_note_chunks("data/raw/P001/notes.pdf")
    print(len(notes))     # expect 3
    print(notes[0])
    print(notes[-1])  
