from corpus import ingest

def _rows(sql, params = ()):
    cn = ingest.connect()
    try: 
        cur = cn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()
    finally:
        cn.close()

def test_idempotent():
    first = ingest.load_all()
    sec = ingest.load_all()
    assert first == sec

def test_pii_not_present():
    ingest.load_all()
    texts = "".join(row[0] for row in _rows("SELECT text FROM note_chunks"))
    assert "Rohan Mehta" not in texts
    assert "9876543210" not in texts

def test_p002_week1_masked():
    ingest.load_all()
    rows = _rows(
        "SELECT text FROM note_chunks WHERE patient_id = %s AND week = %s",
        ("P002", 1),
    )
    assert len(rows) == 1
    text = rows[0][0]
    assert "Rohan Mehta" not in text
    assert "9876543210" not in text
    assert "<PERSON>" in text
    assert "<PHONE_NUMBER>" in text

def test_precision_in_db():
    ingest.load_all()
    freqs = {row[0] for row in _rows("SELECT DISTINCT frequency FROM med_rows")}
    assert "twice daily" in freqs
    assert "every 8 hours" in freqs
    analytes = {row[0] for row in _rows("SELECT DISTINCT analyte FROM lab_rows")}
    assert "Creatinine" in analytes

def test_counts():
    counts = ingest.load_all()
    assert counts == {"lab_rows": 80, "med_rows": 29, "note_chunks": 31}
