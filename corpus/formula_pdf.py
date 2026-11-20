from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def render_formula_pdf(out_path: Path | str) -> None:
    out_file = Path(out_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    
    story = [
        Paragraph("Renal Function Formulas: eGFR and CrCl", styles["Heading1"]),
        Spacer(1, 12),
        Paragraph("eGFR (CKD-EPI 2021)", styles["Heading2"]),
        Paragraph(
            "eGFR = 142 x min(Scr/kappa, 1)^alpha x max(Scr/kappa, 1)^-1.200 x "
            "0.9938^age x 1.012 (if female)",
            styles["BodyText"],
        ),
        Paragraph(
            "kappa = 0.7 for female, 0.9 for male. "
            "alpha = -0.241 for female, -0.302 for male.",
            styles["BodyText"],
        ),
        Paragraph(
            "Scr = serum creatinine in mg/dL. Age in years. "
            "eGFR in mL/min/1.73m2. Normal eGFR is 90 or higher.",
            styles["BodyText"],
        ),
        Spacer(1, 12),
        Paragraph("CrCl (Cockcroft-Gault)", styles["Heading2"]),
        Paragraph(
            "CrCl = ((140 - age) x weight_kg) / (72 x Scr) x 0.85 (if female)",
            styles["BodyText"],
        ),
        Paragraph(
            "CrCl in mL/min. weight_kg in kilograms. "
            "Use this formula when actual body weight dosing is required.",
            styles["BodyText"],
        ),
    ]
    SimpleDocTemplate(str(out_file), pagesize=letter).build(story)

if __name__ == "__main__":
    render_formula_pdf("data/raw/formula/egfr.pdf")
    print("Generated data/raw/formula/egfr.pdf successfully.")
