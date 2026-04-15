from datetime import datetime, timedelta, timezone
import os
import time
import uuid
import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Database imports removed to keep code safe and simple

APP_TITLE = "Maturitní AI Asistentka"

# --- KONFIGURACE PRO GEMMA (ŠKOLNÍ SERVER) ---
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "https://kurim.ithope.eu/v1/chat/completions")
LM_STUDIO_TIMEOUT = int(os.getenv("LM_STUDIO_TIMEOUT", "60"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-k_ILpNLyqBVD-6yqHXzvow")

# Definice českého času
CZ_TIMEZONE = timezone(timedelta(hours=2))

SYSTEM_PROMPT = (
    "Jsi milá a chytrá česká asistentka Mahulina. "
    "Pomáháš studentům s maturitou. "
    "Odpovídej v češtině, stručně a s empatií ✨"
)

DEFAULT_WELCOME = "Ahoj! Jsem tvoje asistentka Mahulina. S čím ti dnes pomůžu s přípravou na maturitu? 🌸"

class ChatPayload(BaseModel):
    prompt: str
    session_id: str = None

app = FastAPI(title=APP_TITLE)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database initialization removed

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    current_cz_time = datetime.now(CZ_TIMEZONE).strftime("%H:%M:%S")
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_title": APP_TITLE,
            "welcome_message": DEFAULT_WELCOME,
            "current_time": current_cz_time,
        },
    )

@app.get("/api/ping")
def ping():
    return {"message": "Systém běží! (pong)", "status": "ok"}

@app.get("/api/status")
def status():
    current_cz_time = datetime.now(CZ_TIMEZONE).strftime("%H:%M:%S")
    return {
        "author": "Mahulina ✨",
        "status": "Online",
        "time": current_cz_time,
        "brain": "Gemma 3 (27B)",
    }

@app.post("/api/chat")
def chat(payload: ChatPayload):
    prompt = payload.prompt.strip()
    if not prompt:
        return JSONResponse(status_code=400, content={"error": "Prompt nesmí být prázdný."})

    session_id = payload.session_id or str(uuid.uuid4())
    
    # History loading removed to bypass database errors

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.append({"role": "user", "content": prompt})

    body = {
        "model": "gemma3:27b",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 800
    }

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            LM_STUDIO_URL,
            json=body,
            headers=headers,
            timeout=LM_STUDIO_TIMEOUT
        )

        if response.status_code != 200:
            return JSONResponse(
                status_code=502,
                content={"error": "AI Server Error.", "details": response.text},
            )

        data = response.json()
        answer = data["choices"][0]["message"]["content"]

        # Database saving removed

        return {"answer": answer, "session_id": session_id}

    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"error": "AI server neodpovídá.", "details": str(e)},
        )

@app.get("/api/history/{session_id}")
def get_history(session_id: str):
    # Returns empty history to satisfy the frontend request without a database
    return {
        "session_id": session_id,
        "messages": []
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)