from corpus.patients import P001
from corpus.parse import extract_lab_rows, extract_med_rows, extract_note_chunks

def test_roundtrip_labs():
    rows = extract_lab_rows("data/raw/P001/labs.pdf")
    expected = P001.labs

    assert len(rows) == len(P001.labs) 
    
    for i, (parsed, expected) in enumerate(zip(rows, P001.labs)):
        assert parsed == expected, f"Mismatch at row {i}"

def test_roundtrip_meds():
    rows = extract_med_rows("data/raw/P001/meds.pdf")
    expected = P001.meds

    assert len(rows) == len(expected)

    for i, (parsed, expected) in enumerate(zip(rows, expected)):
        assert parsed == expected, f"Missing rows {i}"

def test_roundtrip_notes():
    notes = extract_note_chunks("data/raw/P001/notes.pdf")
    # 1. count matches expect 3
    assert len(notes) == len(P001.notes)
    for i, (parsed, expected) in enumerate(zip(notes, P001.notes)):
        assert parsed == expected, f"Mismatch at note {i}"

def test_roundtrip_notes_last_week_present():
    # guards the "final push" bug: if the last week isn't flushed
    # after the loop, week 3 is missing and this fails
    notes = extract_note_chunks("data/raw/P001/notes.pdf")
    assert notes[-1].week == 3
