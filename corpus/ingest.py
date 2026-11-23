import os
from pathlib import Path
import pdfplumber
import psycopg

from corpus.mask import mask_pii
from corpus.parse import extract_lab_rows, extract_med_rows, extract_note_chunks
from corpus.patients import ALL_PATIENTS

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS lab_rows(
    patient_id TEXT, analyte TEXT, value DOUBLE PRECISION , unit TEXT, week INT
);
CREATE TABLE IF NOT EXISTS med_rows(
    patient_id TEXT, name TEXT, dose TEXT, frequency TEXT, week INT
);
CREATE TABLE IF NOT EXISTS note_chunks(
    patient_id TEXT, week INT, kind TEXT, text TEXT 
);
"""

def _load_env() -> None:
    env_path = Path(".env")
    if not env_path.exists():
        return 
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if "=" not in line or line.startswith("#") or not line:
            continue
        k,v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def connect(): 
    _load_env()
    return psycopg.connect(
        host="localhost", 
        user=os.environ.get("POSTGRES_USER"),
        port=5432, 
        dbname= os.environ.get("POSTGRES_DB"),
        password=os.environ.get("POSTGRES_PASSWORD") 
    )


def init_schema(cur) -> None:
    cur.execute(SCHEMA_SQL)

def load_labs(cur):
    rows = []
    for p in ALL_PATIENTS:
        for lab in extract_lab_rows(f"data/raw/{p.id}/labs.pdf"):
            rows.append((p.id, mask_pii(lab.analyte), lab.value, mask_pii(lab.unit), lab.week))
    cur.executemany("INSERT INTO lab_rows VALUES(%s, %s, %s,%s,%s)", rows)

def load_meds(cur):
    rows = []
    for p in ALL_PATIENTS:
        for meds in extract_med_rows(f"data/raw/{p.id}/meds.pdf"):
            rows.append((p.id, mask_pii(meds.name), mask_pii(meds.dose), mask_pii(meds.frequency), meds.week))
    cur.executemany("INSERT INTO med_rows VALUES(%s, %s, %s, %s, %s)", rows)

def load_note_chunks(cur):
    rows = []
    for p in ALL_PATIENTS:
        for notes in extract_note_chunks(f"data/raw/{p.id}/notes.pdf"):
            rows.append((p.id, notes.week, "note", mask_pii(notes.text)))
    cur.executemany("INSERT INTO note_chunks VALUES(%s, %s, %s, %s)", rows)

def load_formula(cur):
    with pdfplumber.open("data/raw/formula/egfr.pdf") as pdf:
        text = pdf.pages[0].extract_text()

    cur.execute("INSERT INTO note_chunks VALUES(%s, %s, %s, %s)", 
                ("GLOBAL", None, "formula", mask_pii(text)),
            )

def load_all():
    _load_env()
    cn = connect()
    try:
        cur = cn.cursor() #cursor object to send sql cmds after establishing connection. 
        init_schema(cur)

        cur.execute(SCHEMA_SQL)
        cur.execute("TRUNCATE lab_rows, med_rows, note_chunks")

        load_labs(cur)
        load_meds(cur)
        load_note_chunks(cur)
        load_formula(cur)

        cn.commit()

        counts = {}
        for table in ("lab_rows", "med_rows", "note_chunks"):
            cur.execute(f"SELECT count(*) from {table}") # saves this in cur's intermal buffer
            counts[table]= cur.fetchone()[0]
        return counts
    finally:
        cn.close()


if __name__ == "__main__":
    print(load_all())

        
        
