from typing import TypedDict
from qa.retriever import get_retriever
from llm import complete
from langgraph.types import interrupt, Command
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver



class State(TypedDict):
    question: str
    chunks: list[dict]
    draft: str
    citations: list[str]
    status: str
    answer: str

def build_my_prompt(question: str, chunks : list[dict]) -> str:
    lines = sorted(chunks, key = lambda c: (c["patient_id"], c["week"] or 0))
    contx = "\n".join(
        f"[{c["patient_id"]}/week={c["week"]}/{c["kind"]}] [{c["text"]}]" for c in lines
    )
    prompt =(
            "Answer only from this chart, Cite as [patient_id/week/kind] if not in the sources say you don't know "
            f"\n Sources : \n{contx}\n\n Question: {question}"
            )
    return prompt

def make_graph(retriever = None):
    retriever = retriever or get_retriever

    async def retrieve(state : State):
        return {"chunks" : await retriever(state["question"], k=3)}

    async def draft(state: State):
        return {
            "draft": complete(build_my_prompt(state["question"], state["chunks"])),
            "citations": [f"{c['patient_id']}/w{c['week']}/{c['kind']}" for c in state["chunks"]],
        }

    async def approve(state: State):
        decision = interrupt({"draft": state["draft"], "citations": state["citations"]})
        if not decision.get("approved"):
            return {"status" : "rejected", "answer" :"Rejected by a human"}
        return {"status": "approved", "answer": decision.get("edits") or state["draft"]}


    sg = StateGraph(State)
    sg.add_node("retrieve", retrieve)
    sg.add_node("draft", draft)
    sg.add_node("approve", approve)
    sg.add_edge("retrieve", "draft")
    sg.add_edge("draft", "approve")
    sg.add_edge("approve", END)
    sg.set_entry_point("retrieve")
    return sg.compile(checkpointer=MemorySaver())




