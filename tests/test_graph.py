import pytest
from corpus import embed as e
from corpus import ingest as i
from qa import graph as g
import uuid
import asyncio
from qa.graph import make_graph
from qa.llm import FIXTURES, complete
from qa.graph import build_my_prompt, make_graph
from corpus.retrieve import search_text
import json
from pathlib import Path
import subprocess
import sys
import os
import time
import socket
from qa.retriever import search_local, search_mcp


GOLDEN_QUESTION = "Why was lisinopril reduced to 5mg?"
DEF_ANSWER = "The dose was reduced because creatinine rose [P001/week=3/note]."

@pytest.fixture(scope="module", autouse=True) # a setup fn that loads all my patient data. and run auto for this file(module).
def _loadall():
    i.load_all()
    e.embed_all()

@pytest.fixture()
def fake_LLM_call(monkeypatch): 
    monkeypatch.setattr(g, "complete", lambda prompt: DEF_ANSWER) #complete fn is in llm.py but imported in graoh so g.complete is called and made to return DEF_ANSWER as "draft" instead od calling LLM APIs during tests


#helper functions
def _cfg():
    return {"configurable": {"thread_id": str(uuid.uuid4())}}

def _ask(graph, cfg):
    return asyncio.run(graph.ainvoke({"question": GOLDEN_QUESTION} ,cfg))

def _resume(graph, cfg, decision):
    from langgraph.types import Command
    return asyncio.run(graph.ainvoke(Command(resume=decision), cfg))

#testing langgraph workflow 

def test_retrieval_for_goldenq(fake_LLM_call):
    res = _ask(make_graph(), _cfg())
    got = [(c["patient_id"] , c["week"]) for c in res["chunks"]]
    assert ("P001", 3) in got 

def test_interrupt_draft_citations(fake_LLM_call):
    res = _ask(make_graph(), _cfg())
    assert "__interrupt__" in res
    payload = res["__interrupt__"][0].value # note both drafta nd citations are stored in payload now 
    assert payload["draft"] == DEF_ANSWER # did our fake llm work?
    assert any("P001" in c for c in payload["citations"]) # whertehr it is citing its sources 

def test_resume_approve(fake_LLM_call):
    graph, cfg = make_graph(), _cfg()
    _ask(graph, cfg)
    res = _resume(graph, cfg, {"approved": True})
    assert res["status"] == "approved"
    assert res["answer"] == DEF_ANSWER

def test_resume_reject(fake_LLM_call):
    graph, cfg = make_graph(), _cfg()
    _ask(graph, cfg)
    res = _resume(graph, cfg, {"approved": False})
    assert res["status"] == "rejected"


def test_resume_edited(fake_LLM_call):
    graph, cfg = make_graph(), _cfg()
    _ask(graph, cfg)
    res = _resume(graph, cfg, {"approved": True, "edits": "Edited answer [P001/week=3/note]"})
    assert res["status"] == "approved"
    assert res["answer"] == "Edited answer [P001/week=3/note]"

#testing replay cache 
# no fake_llm , monkey patch is closed and we are back to the real path, but we only set attrubite using monkey path for test isolation for this FNs

def test_replay_refuse_unknown_prompt(monkeypatch): # checks if unknown prompt dont call apis and raise error
    monkeypatch.setenv("LLM_MODE", "replay")
    with pytest.raises(RuntimeError): #explictly mentioend so test passes if runtimeerror is raised and fails if not 
        complete("this prompt was never recorded")

def test_replay_with_fixtures(monkeypatch): # checks since we have seed_replay for test exclusively, generating hashes and path and compleet which runs live (but here in replay mode) chekcing to ensure consistency and text exists. 
    monkeypatch.setenv("LLM_MODE", "replay") # so complete() reads from disk instead of API
    prompt = build_my_prompt(GOLDEN_QUESTION, search_text(GOLDEN_QUESTION, k=3))
    path = __import__("conftest").seed_replay(prompt, DEF_ANSWER)
    assert complete(prompt) == json.loads(path.read_text())["text"]

# testing MCP and checking if the MCP retrieved texts are same as texts done locally.
# why? - fields could get dropped, connection URLS failing. sorting changing could happen.

def test_mcp_local_graph():
    root = Path(__file__).parent[1] # makes sure it gets the root dir which is "1" folder above tests
    proc = subprocess.Popen( # sub process opened up seperate from the test flow so it doesnt block the main process or mcp server 
        [sys.executable, "-m", "mcp_server.server"],
        env={**os.environ, "MCP_PORT":"8001"},
        cwd=root, 
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ) 
    try:
        deadline = time.time() + 60
        while True:
            try:
                with socket.create_connection(("127.0.0.1", 8001), timeout=1):
                    break
            except OSError:
                if time.time() > deadline:
                    raise TimeoutError("Server is not coming up")
                time.sleep(0.5) # before checking again

        os.environ["MCP_URL"] = "http://127.0.0.1:8001/mcp"

        async def call_both():
            return await search_local(GOLDEN_QUESTION, 3) , await search_mcp(GOLDEN_QUESTION, 3)

        local, remote = asyncio.run(call_both())
        key = lambda rows : [(r["patient_id"], r["week"]) for r in rows]
        assert key(local) == key(remote)
        assert("P001", 3) in key(local)

        graph = make_graph(retriever=search_mcp)
        res = _ask(graph, _cfg())
        got = [(r["patient_id"], r["week"]) for r in res["chunks"]]
        assert ("P001", 3) in got
        assert "__interrupt__" in res


    finally:
        os.environ.pop("MCP_URL", None)
        proc.kill()
        proc.wait(timeout=10)














