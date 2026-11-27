from fastapi.testclient import TestClient # this lest you run fake htt reuest in py memory itself. 

import pytest
from fastapi.testclient import TestClient

from corpus import embed as e
from corpus import ingest as i
from qa import graph as g
from qa.api import app

GOLDEN_Q = "Why was lisinopril reduced to 5mg?"
CANNED = "The dose was reduced because creatinine rose [P001/week=3/note]."


@pytest.fixture(scope="module", autouse=True)
def _load():
    i.load_all()
    e.embed_all()


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setattr(g, "complete", lambda prompt: CANNED)
    return TestClient(app)


def _ask(client):
    r = client.post("/ask", json={"question": GOLDEN_Q})
    assert r.status_code == 200
    return r.json()


def test_health(client):
    assert client.get("/health").json() == {"ok": True}

def test_ask_returns_pending_approval(client):
    body = _ask(client)
    assert body["status"] == "pending_approval"
    assert body["draft"] == CANNED
    assert body["thread_id"]
    assert any("P001" in c for c in body["citations"])


def test_approve_flow(client):
    ask = _ask(client)
    r = client.post("/approve", json={"thread_id": ask["thread_id"], "approved": True})
    body = r.json()
    assert r.status_code == 200
    assert body["status"] == "approved"
    assert body["answer"] == CANNED


def test_reject_flow(client):
    ask = _ask(client)
    body = client.post("/approve", json={"thread_id": ask["thread_id"], "approved": False}).json()
    assert body["status"] == "rejected"


def test_edits_override(client):
    ask = _ask(client)
    body = client.post("/approve", json={
        "thread_id": ask["thread_id"], "approved": True,
        "edits": "Human-edited answer [P001/week=3/note]",
    }).json()
    assert body["status"] == "approved"
    assert body["answer"] == "Human-edited answer [P001/week=3/note]"