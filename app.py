"""Kisan Dost — FastAPI backend serving the chat UI."""

from __future__ import annotations

import uuid
from pathlib import Path
from threading import Lock

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from kisan_dost.agent import KisanDostAgent

load_dotenv()

ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT / "frontend"

app = FastAPI(title="Kisan Dost", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_sessions: dict[str, KisanDostAgent] = {}
_lock = Lock()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    context: dict


def _get_or_create(session_id: str | None) -> tuple[str, KisanDostAgent]:
    with _lock:
        if session_id and session_id in _sessions:
            return session_id, _sessions[session_id]
        sid = session_id or str(uuid.uuid4())
        try:
            agent = KisanDostAgent()
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e)) from e
        _sessions[sid] = agent
        return sid, agent


@app.get("/api/health")
def health() -> dict:
    return {"ok": True, "service": "kisan-dost"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(body: ChatRequest) -> ChatResponse:
    session_id, agent = _get_or_create(body.session_id)
    try:
        reply = agent.chat(body.message.strip())
    except Exception as e:
        err = str(e)
        if "429" in err or "RESOURCE_EXHAUSTED" in err:
            raise HTTPException(
                status_code=429,
                detail="Gemini free quota finished. Wait, or change GEMINI_MODEL in .env.",
            ) from e
        raise HTTPException(status_code=502, detail=err) from e
    return ChatResponse(
        reply=reply,
        session_id=session_id,
        context=agent.get_context().to_dict(),
    )


@app.post("/api/reset")
def reset(session_id: str | None = None) -> dict:
    with _lock:
        if session_id and session_id in _sessions:
            del _sessions[session_id]
    new_id, agent = _get_or_create(None)
    return {"session_id": new_id, "context": agent.get_context().to_dict()}


app.mount("/assets", StaticFiles(directory=FRONTEND), name="assets")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND / "index.html")
