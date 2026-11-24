import pytest

from corpus import embed as e
from corpus import retrieve as r

@pytest.fixture(scope="module", autouse=True)
def _load():
    e.embed_all()          # load_all() may have wiped vectors — re-embed first

GOLDEN = [
    ("Why was lisinopril reduced to 5mg?",              ("P001", 3)),
    ("stopped Losartan started amlodipine",             ("P006", 3)),
    ("switched to Cephalexin after creatinine spiked",  ("P008", 2)),
    ("lowered HCTZ for hyponatremia",                   ("P010", 3)),
    ("eGFR formula",                                    ("GLOBAL", None)),
]

def test_k_hits():
    k = 3
    hits = 0
    for question, expected in GOLDEN:
        results = r.search_text(question, k=k)
        got = [(row["patient_id"], row["week"]) for row in results]
        if expected in got:
            hits += 1
        else:
            print(f"MISS: {question!r} expected {expected}, got {got}")
    print(f"hit@{k} = {hits}/{len(GOLDEN)}")
    assert hits == len(GOLDEN), "golden questions must retrieve right sources"


def test_k_limit_and_order():
    results = r.search_text("creatinine rising", k=3)
    assert len(results) <= 3
    sims = [row["similarity"] for row in results]
    assert sims == sorted(sims, reverse=True)
