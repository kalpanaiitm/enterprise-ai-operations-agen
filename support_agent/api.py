"""Local demonstration API. No authentication, durable storage, or outbound sending."""
import uuid

from fastapi import FastAPI, HTTPException
from langgraph.types import Command
from pydantic import BaseModel, Field

from .workflow import create_graph

app = FastAPI(title="Fictional IT Support Operations Agent", version="0.1.0")
graph = create_graph()


class TicketIn(BaseModel):
    text: str = Field(min_length=10, max_length=2000)


class ReviewIn(BaseModel):
    approved: bool
    edited_response: str | None = Field(default=None, max_length=4000)


def _config(ticket_id: str) -> dict:
    try:
        uuid.UUID(ticket_id)
    except ValueError as exc:
        raise HTTPException(404, "Ticket not found") from exc
    return {"configurable": {"thread_id": ticket_id}}


def _view(ticket_id: str) -> dict:
    snapshot = graph.get_state(_config(ticket_id))
    state = snapshot.values
    if not state or "ticket" not in state:
        raise HTTPException(404, "Ticket not found")
    return {
        "ticket_id": ticket_id,
        "status": state.get("status", "pending_review" if snapshot.next else "unknown"),
        "category": state.get("category"),
        "sensitive": state.get("sensitive"),
        "evidence": state.get("evidence", []),
        "draft": state.get("draft"),
        "model_used": state.get("model_used"),
        "final_response": state.get("final_response"),
        "audit": state.get("audit", []),
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tickets", status_code=201)
def create_ticket(ticket: TicketIn):
    ticket_id = str(uuid.uuid4())
    graph.invoke({"ticket": ticket.text}, _config(ticket_id))
    return _view(ticket_id)


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str):
    return _view(ticket_id)


@app.post("/tickets/{ticket_id}/review")
def review_ticket(ticket_id: str, decision: ReviewIn):
    snapshot = graph.get_state(_config(ticket_id))
    if not snapshot.values or "review" not in snapshot.next:
        raise HTTPException(409, "Ticket is not pending review")
    if decision.approved and decision.edited_response is not None and not decision.edited_response.strip():
        raise HTTPException(422, "Edited response cannot be blank")
    graph.invoke(Command(resume=decision.model_dump()), _config(ticket_id))
    return _view(ticket_id)
