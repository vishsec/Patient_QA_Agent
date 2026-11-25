from mcp_server.formula import egfr, crcl

def test_egfr_female():
    # hand-computed from the PDF formula: scr=1.0, age=60, female → ≈64.5
    assert abs(egfr(1.0, 60, "female") - 64.5) < 1.0

def test_egfr_male():
    # scr=1.0, age=60, male → ≈86.2
    assert abs(egfr(1.0, 60, "male") - 86.2) < 1.0

def test_crcl_male():
    # (140-60)*70/(72*1.0) = 77.8
    assert abs(crcl(1.0, 60, "male", 70) - 77.8) < 0.5

def test_crcl_female_is_85pct():
    assert abs(crcl(1.0, 60, "female", 70) - crcl(1.0, 60, "male", 70) * 0.85) < 0.01

# used AI here to get values and formulas 