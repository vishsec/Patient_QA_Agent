import hashlib , os, json
from pathlib import Path

FIXTURES = Path("tests/fixtures/replay")

def complete(prompt : str) -> str:
    mode = os.environ.get("LLM_MODE", "replay")
    key = hashlib.sha256(prompt.encode()).hexdigest()

    if mode == "replay":
        path = FIXTURES / f"{key}.json"
        if not path.exists():
            raise RuntimeError(f"json file does not exist for prompt: {prompt} in replay mode")
        return json.loads(path.read_text())["text"]

    from google import genai
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    resp = client.models.generate_content(model=os.environ.get("LLM_MODEL", "gemini-2.5-flash"), contents=prompt)
    text = resp.text
    FIXTURES.mkdir(parents=True, exist_ok=True)
    (FIXTURES / f"{key}.json").write_text(json.dumps({"text":text, "prompt": prompt}, indent=2))
    return text