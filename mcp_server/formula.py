def egfr(scr: float, age: int, sex: str) -> float:
    #CKD-EPI 2021 (no weight needed). scr in mg/dL
    female = sex.lower().startswith("f")
    kappa = 0.7 if female else 0.9
    alpha = -0.241 if female else -0.302
    base = scr / kappa
    value = (142 * min(base, 1) ** alpha * max(base, 1) ** -1.200
             * 0.9938 ** age)
    if female:
        value *= 1.012
    return value

def crcl(scr: float, age: int, sex: str, weight_kg: float) -> float:
    #Cockcroft-Gault (weight-based, for drug dosing).
    value = ((140 - age) * weight_kg) / (72 * scr)
    if sex.lower().startswith("f"):
        value *= 0.85
    return value

# used AI to get values and formulas