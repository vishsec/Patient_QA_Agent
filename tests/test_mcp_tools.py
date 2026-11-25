import asyncio

from mcp_server import server as sv 
from corpus import embed as e
from corpus import ingest as i

def _load():
    i.load_all()
    e.embed_all()

def load_all_tools():
    tools = asyncio.run(sv.server.list_tools())
    assert sorted(t.name for t in tools) == ["get_chunks","run_formula", "search"]

def test_search_hits_golden():
    _load()
    hits = sv.search("why was lisinopril reduced", k=3)
    assert len(hits) == 3
    assert ("P001", 3) in [(h["patient_id"], h["week"]) for h in hits]

def test_get_chunk_masks_pii():
    _load()
    text = sv.get_chunks("P002", 1, "note")
    assert "<PHONE_NUMBER>" in text and "Rohan Mehta" not in text

def test_get_chunk_formula_null_week():
    _load()
    assert "eGFR" in sv.get_chunks("GLOBAL", None, "formula")

def test_run_formula_with_and_without_weight():
    _load()
    out = sv.run_formula(scr=1.4, age=65, sex="male")
    assert out["egfr"] > 0 and "crcl" not in out and "eGFR" in out["source"]
    out2 = sv.run_formula(scr=1.4, age=65, sex="male", weight_kg=70)
    assert out2["crcl"] > 0

