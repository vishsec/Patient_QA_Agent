from mcp.server.mcpserver import MCPServer
from corpus.ingest import connect
from corpus.retrieve import search_text
from mcp_server.formula import egfr, crcl

server = MCPServer("patient_qa")

def get_chunks(patient_id : str, week : int | None, kind : str) -> str:
    cn = connect()
    try:
        cur = cn.cursor()
        cur.execute(
            "SELECT TEXT from note_chunks WHERE patient_id=%s AND kind=%s AND week IS NOT DISTINCT FROM %s",
            (patient_id, kind, week),
        )
        row = cur.fetchone()
        return row[0] if row else f"No text found for patient id {patient_id} on kind {kind} for the week {week}"
    finally:
        cn.close()

def search(query: str, k: int=3) -> list[dict]:
    return search_text(query, k)

def run_formula(scr: float, age: int, sex:str, weight_kg: int | None = None) -> dict:
    out = {"egfr": round(egfr(scr, age, sex), 1) , "formula":"CKD-EPI 2021"}
    if weight_kg is not None:
        out["crcl"] = round(crcl(scr, age, sex, weight_kg), 1)
        out["crcl_formula"] = "Cockcroft-gault"
    out["source"] = get_chunks("GLOBAL", None, "formula")
    return out


server.tool()(get_chunks)
server.tool()(search)
server.tool()(run_formula)

if __name__ == "__main__":
    import os
    server.run(transport="streamable-http", host="0.0.0.0", port=int(os.environ.get("MCP_PORT","8080"))) 



