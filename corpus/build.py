from pathlib import Path

from corpus.formula_pdf import render_formula_pdf
from corpus.lab_pdf import render_labs_pdf
from corpus.meds_pdf import render_meds_pdf
from corpus.notes_pdf import render_notes_pdf
from corpus.patients import ALL_PATIENTS

BASE = Path("data/raw")

def main() -> None:
    written = 0
    for p in ALL_PATIENTS:
        render_labs_pdf(p, BASE/p.id/"labs.pdf")
        render_meds_pdf(p, BASE/p.id/"meds.pdf")
        render_notes_pdf(p, BASE/p.id/"notes.pdf")
        written += 3
    render_formula_pdf(BASE / "formula" / "egfr.pdf")
    written +=1
    print(f"successfully generated: {written} files under {BASE}")

if __name__ == "__main__":
    main()