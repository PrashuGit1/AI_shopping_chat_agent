from fastapi import FastAPI, Request
from pydantic import BaseModel
import sqlite3
import re
from typing import List, Optional, Dict
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from backend.nlu import parse_intent
from backend.recommender import query_phones, compare_models
from backend.safety import check_user_message

app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

DB_PATH = 'phones.db'

class ChatRequest(BaseModel):
    message: str
    mode: Optional[str] = 'recommend'  # 'recommend' or 'compare'
    compare_models: Optional[List[str]] = None

@app.post('/chat')
async def chat(req: ChatRequest):
    # Safety check
    safe, reason = check_user_message(req.message)
    if not safe:
        return JSONResponse(status_code=400, content={'error': 'Request refused', 'reason': reason})

    intent = parse_intent(req.message)

    if req.mode == 'compare':
        # If user requested compare by listing models, use those; otherwise use intent to pick 2-3
        models = req.compare_models or intent.get('models')
        if not models:
            return {'error': 'No models specified for comparison.'}
        results = compare_models(DB_PATH, models)
        return {'type': 'comparison', 'items': results}

    # normal recommendation flow
    phones = query_phones(DB_PATH, intent)
    return {'type': 'recommendation', 'intent': intent, 'items': phones}

@app.get('/')
async def index():
    return FileResponse('../frontend/index.html')