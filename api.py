from datetime import datetime, timedelta, timezone
import os
import time
import uuid
import requests
import psycopg2  
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

APP_TITLE = "Maturitní AI Asistentka"

LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "https://kurim.ithope.eu/v1/chat/completions")
LM_STUDIO_TIMEOUT = int(os.getenv("LM_STUDIO_TIMEOUT", "60"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CZ_TIMEZONE = timezone(timedelta(hours=2))

DB_URL = os.getenv("DATABASE_URL", "postgresql://mahulina:heslo123@db:5432/mahulina_db")

SYSTEM_PROMPT = (
    "Jsi milá a chytrá česká asistentka Mahulina. "
    "Pomáháš studentům s maturitou. "
    "Odpovídej v češtině, stručně a s empatií ✨"
)

DEFAULT_WELCOME = "Ahoj! Jsem tvoje asistentka Mahulina. S čím ti dnes pomůžu s přípravou na maturitu? 🌸"

def init_db():

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS messages (sid TEXT, role TEXT, content TEXT, ts TIMESTAMP)")
    conn.commit()
    cur.close()
    conn.close()

def save_msg(sid, role, content):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (sid, role, content, ts) VALUES (%s, %s, %s, %s)", 
                 (sid, role, content, datetime.now(CZ_TIMEZONE)))
    conn.commit()
    cur.close()
    conn.close()

def get_msgs(sid):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT role, content FROM messages WHERE sid = %s ORDER BY ts ASC", (sid,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"role": r, "content": c} for r, c in rows]

init_db()

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
    
    # 1. Uložit zprávu uživatele
    save_msg(session_id, "user", prompt)

    history = get_msgs(session_id)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in history:
        messages.append({"role": m["role"], "content": m["content"]})

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

        save_msg(session_id, "assistant", answer)

        return {"answer": answer, "session_id": session_id}

    except Exception as e:
        return {"answer": "Omlouvám se, Mahulina teď odpočívá. Zkus to za chvilku! ✨", "session_id": session_id}

@app.get("/api/history/{session_id}")
def get_history(session_id: str):
    msgs = get_msgs(session_id)
    formatted = [{"sender": m["role"], "content": m["content"]} for m in msgs]
    return {
        "session_id": session_id,
        "messages": formatted
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
