from fastapi import FastAPI
from qa.graph import make_graph
from pydantic import BaseModel
import uuid
from langgraph.types import Command

app = FastAPI(title="PatientQA")
graph = make_graph()

class AskReq(BaseModel): # can be new convo
    question: str
    thread_id: str | None = None

class ApproveReq(BaseModel): # to resume conversations
    thread_id: str
    approved: bool
    edits: str | None = None

@app.post("/ask")
async def ask(req: AskReq):
    tid = req.thread_id or str(uuid.uuid4())
    cfg = {"configurable": {"thread_id": tid}} # inserts thread_od in langgraoh's config dir so functions like MemmroySaver() can use this to save states
    result = await graph.ainvoke({"question": req.question}, cfg) #runs graph async
    if "__interrupt__" in result:
        p = result["__interrupt__"][0].value #when intterupt in place (check approve fn) it has two fields draft and citataions now p comtians those values 
        return {"thread_id": tid, "status":"pending_approval", **p} # **p just attced the draft and citataions k-v pairs to the existing dict
    return {"thread_id": tid, "status": result.get("status"), "answer": result.get("answer")} # this return isnt reached since my graoh has nteerupt only when no itetrupts this is returned. 


@app.post("/approve")
async def approve(req : ApproveReq):
    cfg = {"configurable": {"thread_id": req.thread_id}} # Memory Saver() loads back the state. 
    result = graph.ainvoke(
        Command(resume={"approved": req.approved, "edits": req.edits}), # decision.get checks for "approved" in approve fn of graph
        cfg)
    return {"thread_id": req.thread_id, "status": result.get("status"), "answer": result.get("answer")}

@app.get("/health")
def health():
    return {"ok": True}




