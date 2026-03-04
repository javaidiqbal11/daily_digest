"""
DeepAgent Web Application
A modern FastAPI-based web interface for interacting with the DeepAgent system.
"""

import sys
import os
import json
import asyncio
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

from config import config
from utils.logger import logger
from utils.helpers import create_session_id, extract_final_response


# ─── FastAPI App ─────────────────────────────────────────────────────────────
app = FastAPI(
    title="DeepAgent",
    description="Deep Research Agent powered by LangChain",
    version="1.0.0",
)

# Mount static files
STATIC_DIR = Path(__file__).parent / "static"
TEMPLATES_DIR = Path(__file__).parent / "templates"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
(STATIC_DIR / "css").mkdir(parents=True, exist_ok=True)
(STATIC_DIR / "js").mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# ─── In-Memory State ────────────────────────────────────────────────────────
agents_cache: dict = {}
chat_history: dict[str, list] = {}


# ─── Request / Response Models ──────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    agent_type: str = "research"
    session_id: str = ""


class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str
    agent_type: str


# ─── Agent Factory ──────────────────────────────────────────────────────────
def get_or_create_agent(agent_type: str):
    """Get cached agent or create a new one."""
    if agent_type not in agents_cache:
        logger.info(f"Creating {agent_type} agent for web UI...")
        if agent_type == "research":
            from agents.research_agent import create_research_agent
            agents_cache[agent_type] = create_research_agent()
        elif agent_type == "code":
            from agents.code_agent import create_code_agent
            agents_cache[agent_type] = create_code_agent()
        elif agent_type == "general":
            from agents.general_agent import create_general_agent
            agents_cache[agent_type] = create_general_agent()
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
    return agents_cache[agent_type]


# ─── Routes ─────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Serve the main web UI."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle chat messages."""
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    # Generate session ID if not provided
    session_id = request.session_id or create_session_id()
    
    try:
        # Get or create agent
        agent = get_or_create_agent(request.agent_type)
        
        # Run agent
        config_dict = {"configurable": {"thread_id": session_id}}
        result = agent.invoke(
            {"messages": [{"role": "user", "content": request.message}]},
            config=config_dict,
        )
        
        response_text = extract_final_response(result)
        
        # Store in chat history
        if session_id not in chat_history:
            chat_history[session_id] = []
        chat_history[session_id].append({
            "role": "user",
            "content": request.message,
            "timestamp": datetime.now().isoformat(),
        })
        chat_history[session_id].append({
            "role": "assistant",
            "content": response_text,
            "timestamp": datetime.now().isoformat(),
        })
        
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            agent_type=request.agent_type,
        )
        
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history/{session_id}")
async def get_history(session_id: str):
    """Get chat history for a session."""
    history = chat_history.get(session_id, [])
    return JSONResponse(content={"session_id": session_id, "messages": history})


@app.post("/api/clear/{session_id}")
async def clear_session(session_id: str):
    """Clear chat history for a session."""
    if session_id in chat_history:
        del chat_history[session_id]
    return JSONResponse(content={"status": "cleared", "session_id": session_id})


@app.get("/api/reports")
async def get_reports():
    """List all saved reports."""
    from tools.file_tools import list_reports
    result = list_reports()
    return JSONResponse(content={"reports": result})


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse(content={
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    })


# ─── Entry Point ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info(f"🌐 Starting DeepAgent Web UI on http://{config.web.host}:{config.web.port}")
    uvicorn.run(
        "web_app:app",
        host=config.web.host,
        port=config.web.port,
        reload=True,
        log_level="info",
    )
