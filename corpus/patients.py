from dataclasses import dataclass, field

@dataclass
class Labs:
    analyte: str
    value: float
    unit: str
    week: int

@dataclass
class Meds:
    name: str
    dose: str
    frequency: str
    week: int

@dataclass
class Note:
    week: int
    text: str

@dataclass
class Patient:
    id: str
    age: int
    sex: str
    labs: list[Labs]
    meds: list[Meds]
    notes: list[Note]

GOLDEN_IDS = {"P008","P009","P010"}

# P001 = Patient(id = "POO1", age=60, sex="male", labs=[Labs(analyte="Creatinine", value=1.1, unit="mg/dL", week=1),
#                                                         Labs(analyte="Creatinine", value=1.2, unit="mg/dL", week=2),
#                                                         Labs(analyte="Creatinine", value=1.4, unit="mg/dL", week=3)],
#                                                     meds = [Meds(name="", dose="",frequency="",week=1),
#                                                                 Meds(name="", dose="",frequency="",week=2),
#                                                                 Meds(name="", dose="",frequency="",week=3)],
#                                                         notes = [Note(week=1,text=""),Note(week=1,text=""),Note(week=1,text="")])

P001 = Patient(
    id="P001",
    age=60,
    sex="male",
    labs=[
        Labs(analyte="Creatinine", value=1.1, unit="mg/dL", week=1),
        Labs(analyte="Potassium", value=4.3, unit="mmol/L", week=1),
        Labs(analyte="Creatinine", value=1.2, unit="mg/dL", week=2),
        Labs(analyte="Potassium", value=4.6, unit="mmol/L", week=2),
        Labs(analyte="Creatinine", value=1.4, unit="mg/dL", week=3),
        Labs(analyte="Potassium", value=5.1, unit="mmol/L", week=3),
        Labs(analyte="Creatinine", value=1.3, unit="mg/dL", week=5),
        Labs(analyte="Potassium", value=4.7, unit="mmol/L", week=5),
    ],
    meds=[
        Meds(name="Lisinopril", dose="10mg", frequency="once daily", week=1),
        Meds(name="Lisinopril", dose="10mg", frequency="once daily", week=2),
        Meds(name="Lisinopril", dose="5mg", frequency="once daily", week=3),
    ],
    notes=[
        Note(week=1, text="Started Lisinopril 10mg. Baseline Creatinine 1.1 mg/dL and Potassium 4.3 mmol/L."),
        Note(week=2, text="Mild bump in Creatinine to 1.2 mg/dL; patient remains asymptomatic."),
        Note(week=3, text="Creatinine rose to 1.4 mg/dL and Potassium reached 5.1 mmol/L; reduced Lisinopril to 5mg."),
    ],
)

P002 = Patient(
    id="P002",
    age=45,
    sex="female",
    labs=[
        Labs(analyte="Creatinine", value=0.8, unit="mg/dL", week=1),
        Labs(analyte="BUN", value=14, unit="mg/dL", week=1),
        Labs(analyte="Creatinine", value=0.9, unit="mg/dL", week=2),
        Labs(analyte="BUN", value=15, unit="mg/dL", week=2),
        Labs(analyte="Creatinine", value=0.8, unit="mg/dL", week=3),
        Labs(analyte="BUN", value=13, unit="mg/dL", week=3),
        Labs(analyte="Creatinine", value=0.7, unit="mg/dL", week=5),
        Labs(analyte="BUN", value=12, unit="mg/dL", week=5),
    ],
    meds=[
        Meds(name="Metformin", dose="500mg", frequency="twice daily", week=1),
        Meds(name="Metformin", dose="500mg", frequency="twice daily", week=2),
        Meds(name="Metformin", dose="1000mg", frequency="twice daily", week=3),
    ],
    notes=[
        Note(week=1, text="Initiated Metformin 500mg. Normal renal baseline with Creatinine 0.8 mg/dL and BUN 14 mg/dL."),
        Note(week=2, text="Tolerating medication well without GI upset; Creatinine 0.9 mg/dL."),
        Note(week=3, text="Renal function stable at Creatinine 0.8 mg/dL; increased Metformin to 1000mg."),
    ],
)

P003 = Patient(
    id="P003",
    age=72,
    sex="male",
    labs=[
        Labs(analyte="Creatinine", value=1.5, unit="mg/dL", week=1),
        Labs(analyte="BUN", value=24, unit="mg/dL", week=1),
        Labs(analyte="Creatinine", value=1.8, unit="mg/dL", week=2),
        Labs(analyte="BUN", value=32, unit="mg/dL", week=2),
        Labs(analyte="Creatinine", value=1.6, unit="mg/dL", week=3),
        Labs(analyte="BUN", value=27, unit="mg/dL", week=3),
        Labs(analyte="Creatinine", value=1.4, unit="mg/dL", week=5),
        Labs(analyte="BUN", value=21, unit="mg/dL", week=5),
    ],
    meds=[
        Meds(name="Furosemide", dose="40mg", frequency="once daily", week=1),
        Meds(name="Furosemide", dose="40mg", frequency="once daily", week=2),
        Meds(name="Furosemide", dose="20mg", frequency="once daily", week=3),
    ],
    notes=[
        Note(week=1, text="Lower extremity edema noted; started Furosemide 40mg with baseline Creatinine 1.5 mg/dL."),
        Note(week=2, text="Dehydration noted as BUN climbed to 32 mg/dL and Creatinine hit 1.8 mg/dL."),
        Note(week=3, text="Creatinine improved to 1.6 mg/dL; halved Furosemide to 20mg and encouraged fluids."),
    ],
)

P004 = Patient(
    id="P004",
    age=34,
    sex="female",
    labs=[
        Labs(analyte="Creatinine", value=0.7, unit="mg/dL", week=1),
        Labs(analyte="Sodium", value=140, unit="mmol/L", week=1),
        Labs(analyte="Creatinine", value=0.7, unit="mg/dL", week=2),
        Labs(analyte="Sodium", value=139, unit="mmol/L", week=2),
        Labs(analyte="Creatinine", value=0.8, unit="mg/dL", week=3),
        Labs(analyte="Sodium", value=141, unit="mmol/L", week=3),
        Labs(analyte="Creatinine", value=0.7, unit="mg/dL", week=5),
        Labs(analyte="Sodium", value=140, unit="mmol/L", week=5),
    ],
    meds=[
        Meds(name="Ibuprofen", dose="400mg", frequency="every 8 hours", week=1),
        Meds(name="Ibuprofen", dose="400mg", frequency="as needed", week=2),
        Meds(name="Acetaminophen", dose="500mg", frequency="as needed", week=3),
    ],
    notes=[
        Note(week=1, text="Acute back pain; prescribed Ibuprofen 400mg with baseline Creatinine 0.7 mg/dL."),
        Note(week=2, text="Pain improving; Sodium 139 mmol/L and Creatinine unchanged at 0.7 mg/dL."),
        Note(week=3, text="Creatinine ticked up to 0.8 mg/dL; switched to Acetaminophen 500mg to avoid NSAID strain."),
    ],
)

P005 = Patient(
    id="P005",
    age=55,
    sex="male",
    labs=[
        Labs(analyte="Creatinine", value=1.0, unit="mg/dL", week=1),
        Labs(analyte="eGFR", value=82, unit="mL/min", week=1),
        Labs(analyte="Creatinine", value=1.1, unit="mg/dL", week=2),
        Labs(analyte="eGFR", value=74, unit="mL/min", week=2),
        Labs(analyte="Creatinine", value=1.0, unit="mg/dL", week=3),
        Labs(analyte="eGFR", value=82, unit="mL/min", week=3),
        Labs(analyte="Creatinine", value=1.1, unit="mg/dL", week=5),
        Labs(analyte="eGFR", value=74, unit="mL/min", week=5),
    ],
    meds=[
        Meds(name="Atorvastatin", dose="20mg", frequency="once daily", week=1),
        Meds(name="Atorvastatin", dose="20mg", frequency="once daily", week=2),
        Meds(name="Atorvastatin", dose="20mg", frequency="once daily", week=3),
    ],
    notes=[
        Note(week=1, text="Started Atorvastatin 20mg; baseline Creatinine 1.0 mg/dL and eGFR 82 mL/min."),
        Note(week=2, text="No myalgias; Creatinine 1.1 mg/dL with eGFR 74 mL/min."),
        Note(week=3, text="Labs steady at Creatinine 1.0 mg/dL and eGFR 82 mL/min; continuing current dose."),
    ],
)

P006 = Patient(
    id="P006",
    age=68,
    sex="female",
    labs=[
        Labs(analyte="Creatinine", value=1.3, unit="mg/dL", week=1),
        Labs(analyte="Potassium", value=4.5, unit="mmol/L", week=1),
        Labs(analyte="Creatinine", value=1.5, unit="mg/dL", week=2),
        Labs(analyte="Potassium", value=4.9, unit="mmol/L", week=2),
        Labs(analyte="Creatinine", value=1.7, unit="mg/dL", week=3),
        Labs(analyte="Potassium", value=5.3, unit="mmol/L", week=3),
        Labs(analyte="Creatinine", value=1.2, unit="mg/dL", week=5),
        Labs(analyte="Potassium", value=4.4, unit="mmol/L", week=5),
    ],
    meds=[
        Meds(name="Losartan", dose="50mg", frequency="once daily", week=1),
        Meds(name="Losartan", dose="50mg", frequency="once daily", week=2),
        Meds(name="Amlodipine", dose="5mg", frequency="once daily", week=3),
    ],
    notes=[
        Note(week=1, text="Stage 3a CKD baseline: Creatinine 1.3 mg/dL, Potassium 4.5 mmol/L on Losartan 50mg."),
        Note(week=2, text="Creatinine climbed to 1.5 mg/dL and Potassium to 4.9 mmol/L; scheduled repeat labs."),
        Note(week=3, text="Creatinine peaked at 1.7 mg/dL with Potassium 5.3 mmol/L; stopped Losartan and started Amlodipine 5mg."),
    ],
)

P007 = Patient(
    id="P007",
    age=50,
    sex="male",
    labs=[
        Labs(analyte="Creatinine", value=0.9, unit="mg/dL", week=1),
        Labs(analyte="BUN", value=16, unit="mg/dL", week=1),
        Labs(analyte="Creatinine", value=1.0, unit="mg/dL", week=2),
        Labs(analyte="BUN", value=18, unit="mg/dL", week=2),
        Labs(analyte="Creatinine", value=0.9, unit="mg/dL", week=3),
        Labs(analyte="BUN", value=15, unit="mg/dL", week=3),
        Labs(analyte="Creatinine", value=1.0, unit="mg/dL", week=5),
        Labs(analyte="BUN", value=17, unit="mg/dL", week=5),
    ],
    meds=[
        Meds(name="Omeprazole", dose="20mg", frequency="once daily", week=1),
        Meds(name="Omeprazole", dose="20mg", frequency="once daily", week=2),
        Meds(name="Omeprazole", dose="20mg", frequency="once daily", week=3),
    ],
    notes=[
        Note(week=1, text="Started Omeprazole 20mg for reflux; baseline Creatinine 0.9 mg/dL and BUN 16 mg/dL."),
        Note(week=2, text="Reflux resolved; Creatinine 1.0 mg/dL and BUN 18 mg/dL."),
        Note(week=3, text="Renal panel normal at Creatinine 0.9 mg/dL; plan to taper Omeprazole after week 4."),
    ],
)

P008 = Patient(
    id="P008",
    age=79,
    sex="female",
    labs=[
        Labs(analyte="Creatinine", value=1.4, unit="mg/dL", week=1),
        Labs(analyte="Potassium", value=4.4, unit="mmol/L", week=1),
        Labs(analyte="Creatinine", value=1.9, unit="mg/dL", week=2),
        Labs(analyte="Potassium", value=5.2, unit="mmol/L", week=2),
        Labs(analyte="Creatinine", value=1.5, unit="mg/dL", week=3),
        Labs(analyte="Potassium", value=4.6, unit="mmol/L", week=3),
        Labs(analyte="Creatinine", value=1.3, unit="mg/dL", week=5),
        Labs(analyte="Potassium", value=4.3, unit="mmol/L", week=5),
    ],
    meds=[
        Meds(name="Trimethoprim", dose="100mg", frequency="twice daily", week=1),
        Meds(name="Cephalexin", dose="500mg", frequency="twice daily", week=2),
    ],
    notes=[
        Note(week=1, text="Initiated Trimethoprim 100mg for UTI; baseline Creatinine 1.4 mg/dL and Potassium 4.4 mmol/L."),
        Note(week=2, text="Creatinine spiked to 1.9 mg/dL and Potassium to 5.2 mmol/L; switched to Cephalexin 500mg."),
        Note(week=3, text="Infection cleared; Creatinine dropped to 1.5 mg/dL and antibiotics stopped."),
    ],
)

P009 = Patient(
    id="P009",
    age=41,
    sex="male",
    labs=[
        Labs(analyte="Creatinine", value=1.1, unit="mg/dL", week=1),
        Labs(analyte="Sodium", value=138, unit="mmol/L", week=1),
        Labs(analyte="Creatinine", value=1.1, unit="mg/dL", week=2),
        Labs(analyte="Sodium", value=137, unit="mmol/L", week=2),
        Labs(analyte="Creatinine", value=1.2, unit="mg/dL", week=3),
        Labs(analyte="Sodium", value=135, unit="mmol/L", week=3),
        Labs(analyte="Creatinine", value=1.0, unit="mg/dL", week=5),
        Labs(analyte="Sodium", value=138, unit="mmol/L", week=5),
    ],
    meds=[
        Meds(name="Sertraline", dose="50mg", frequency="once daily", week=1),
        Meds(name="Sertraline", dose="50mg", frequency="once daily", week=2),
        Meds(name="Sertraline", dose="100mg", frequency="once daily", week=3),
    ],
    notes=[
        Note(week=1, text="Started Sertraline 50mg; baseline Sodium 138 mmol/L and Creatinine 1.1 mg/dL."),
        Note(week=2, text="Tolerating well; Sodium 137 mmol/L and Creatinine 1.1 mg/dL."),
        Note(week=3, text="Sodium at 135 mmol/L and Creatinine 1.2 mg/dL; titrated Sertraline to 100mg."),
    ],
    )
P010 = Patient(
    id="P010",
    age=63,
    sex="female",
    labs=[
        Labs(analyte="Creatinine", value=0.9, unit="mg/dL", week=1),
        Labs(analyte="Sodium", value=141, unit="mmol/L", week=1),
        Labs(analyte="Creatinine", value=1.0, unit="mg/dL", week=2),
        Labs(analyte="Sodium", value=136, unit="mmol/L", week=2),
        Labs(analyte="Creatinine", value=1.1, unit="mg/dL", week=3),
        Labs(analyte="Sodium", value=133, unit="mmol/L", week=3),
        Labs(analyte="Creatinine", value=0.9, unit="mg/dL", week=5),
        Labs(analyte="Sodium", value=139, unit="mmol/L", week=5),
    ],
    meds=[
        Meds(name="Hydrochlorothiazide", dose="25mg", frequency="once daily", week=1),
        Meds(name="Hydrochlorothiazide", dose="25mg", frequency="once daily", week=2),
        Meds(name="Hydrochlorothiazide", dose="12.5mg", frequency="once daily", week=3),
    ],
    notes=[
        Note(week=1, text="Started Hydrochlorothiazide 25mg; baseline Sodium 141 mmol/L and Creatinine 0.9 mg/dL."),
        Note(week=2, text="Sodium dipped to 136 mmol/L and Creatinine rose to 1.0 mg/dL."),
        Note(week=3, text="Mild hyponatremia at Sodium 133 mmol/L with Creatinine 1.1 mg/dL; lowered HCTZ to 12.5mg."),
    ],
)

ALL_PATIENTS = [P001, P002, P003, P004, P005, P006, P007, P008, P009, P010]