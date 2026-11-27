#deterministic testing of LLMs (Record and replay ficture) 
#Basially tests my LangGraph RAG pipeline, withiut the tokens or non-deterministic AI responses for the same prompt.

import hashlib
import json
import os
from pathlib import Path

os.environ.setdefault("LLM_MODE", "replay")
os.environ.setdefault("RETRIEVER", "local")

FIXTURES =Path(__file__).parent / "fixtures" / "replay"

def pytest_configure(config):
    config.addinivalue_line("markers", "live : no LLM API calls are allowed in CI") # add ini value since ini was a separte file before for pytest.ini for config we can add directly here withiut needinga sep file 

def seed_replay(prompt: str, text:str):
    key = hashlib.sha256(prompt.encode()).hexdigest()
    path = FIXTURES / f"{key}.json"
    if not path.exists():
        FIXTURES.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"text": text, "prompt": prompt}, indent=2))
    return path

