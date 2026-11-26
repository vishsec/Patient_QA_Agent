import os
from corpus.retrieve import search_text

async def search_local(query: str, k: int=3) -> list[dict]: #for top 3
    return search_text(query, k)

async def search_mcp(query: str, k :int=3) -> list[dict]:
    from mcp import ClientSession
    from mcp.client.streamable_http import streamable_http_client

    url = os.environ.get("MCP_URL", "http://127.0.0.1:8000/mcp")
    async with streamable_http_client(url) as (read, write): # open te connection
        async with ClientSession(read,write) as session: # perform ops on the connection 
            await session.initialize() # handshake with server
            result = await session.call_tool("search", {"query": query, "k": k})
            return _parse(result)

def _parse(result) -> list[dict]:
    sc = result.structured_content or {}
    if isinstance(sc, dict) and "result" in sc: #isinstanc checks if sc is in dict format
        return sc["result"]
    raise RuntimeError(f"Unexpected MCP payload {str(sc)[:200]}")

RETRIEVERS = {"local": search_local, "mcp": search_mcp}

def get_retrievers():
    return RETRIEVERS(os.environ.get("search_state", "local"))





