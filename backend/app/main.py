import os
import uuid
import logging
from contextlib import asynccontextmanager
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from .scripts import SCRIPTS, LANGUAGE_NAMES
from .intent import detect_intent
from .ippb_mock import get_balance, apply_loan, get_nearby_branches
from .voice import transcribe, load_asr
from .tts import text_to_speech
from .compliance import generate_accessibility_report, IS_17802_RULES, audit_url
from fastapi.responses import HTMLResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AUDIO_CONTENT_TYPE = "audio/mpeg"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting OSAM Voice Banking Server...")
    load_asr()
    yield
    logger.info("Shutting down OSAM Voice Banking Server...")


app = FastAPI(
    title="OSAM Voice Banking API",
    description="Voice-enabled banking system for IPPB integration — Hindi, Tamil, English",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProcessVoiceRequest(BaseModel):
    audio: Optional[str] = None
    text: Optional[str] = None
    language: str = "hi"
    session_id: Optional[str] = None


class ProcessVoiceResponse(BaseModel):
    intent: str
    transcript: Optional[str] = None
    response_text: str
    requires_input: bool
    session_id: str
    audio_url: Optional[str] = None


class BalanceRequest(BaseModel):
    account_number: str
    language: str = "hi"


class BalanceResponse(BaseModel):
    balance: Optional[float]
    response_text: str
    audio_url: Optional[str] = None


class LoanApplyRequest(BaseModel):
    amount: float
    purpose: str
    language: str = "hi"


class LoanApplyResponse(BaseModel):
    application_id: str
    status: str
    response_text: str
    audio_url: Optional[str] = None


class BranchRequest(BaseModel):
    location: str
    language: str = "hi"


class BranchResponse(BaseModel):
    branches: list
    response_text: str
    audio_url: Optional[str] = None


class ScriptsResponse(BaseModel):
    language: str
    scripts: dict


class ComplianceResponse(BaseModel):
    standard: str
    total_rules: int
    rules: list


class ComplianceAuditRequest(BaseModel):
    url: str


SESSION_STORE: dict[str, dict] = {}


def _get_script(key: str, lang: str, **kwargs) -> str:
    scripts = SCRIPTS.get(lang, SCRIPTS["en"])
    template = scripts.get(key, scripts["error"])
    return template.format(**kwargs) if kwargs else template


def _generate_audio(text: str, lang: str) -> Optional[str]:
    audio_bytes = text_to_speech(text, lang)
    if audio_bytes is None:
        return None
    audio_id = uuid.uuid4().hex
    SESSION_STORE[f"audio_{audio_id}"] = audio_bytes
    return f"/api/audio/{audio_id}"


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "OSAM Voice Banking", "version": "1.0.0"}


@app.get("/api/languages")
async def list_languages():
    return {"languages": [{"code": k, "name": v} for k, v in LANGUAGE_NAMES.items()]}


@app.get("/api/scripts/{language}")
async def get_scripts(language: str):
    if language not in SCRIPTS:
        raise HTTPException(status_code=404, detail=f"Language '{language}' not supported")
    return ScriptsResponse(language=language, scripts=SCRIPTS[language])


@app.post("/api/voice/process", response_model=ProcessVoiceResponse)
async def process_voice(req: ProcessVoiceRequest):
    lang = req.language if req.language in SCRIPTS else "en"
    session_id = req.session_id or uuid.uuid4().hex

    transcript = req.text
    if req.audio:
        transcript = "audio_input"
    elif not transcript:
        transcript = ""

    if not transcript and req.audio:
        transcript = "voice command received"

    intent = detect_intent(transcript, lang)

    SESSION_STORE[session_id] = {"intent": intent, "language": lang, "step": intent}

    response_text = _get_script("help", lang)
    requires_input = True

    if intent == "balance":
        response_text = _get_script("balance_prompt", lang)
        requires_input = True
    elif intent == "loan":
        response_text = _get_script("loan_purpose_prompt", lang)
        requires_input = True
    elif intent == "branch":
        response_text = _get_script("branch_prompt_location", lang)
        requires_input = True
    elif intent == "goodbye":
        response_text = _get_script("goodbye", lang)
        requires_input = False
    elif intent == "help" or intent == "unknown":
        response_text = _get_script("help", lang) + " " + _get_script("main_menu", lang)
        requires_input = True

    audio_url = _generate_audio(response_text, lang)

    return ProcessVoiceResponse(
        intent=intent,
        transcript=transcript,
        response_text=response_text,
        requires_input=requires_input,
        session_id=session_id,
        audio_url=audio_url,
    )


@app.post("/api/balance", response_model=BalanceResponse)
async def check_balance(req: BalanceRequest):
    lang = req.language if req.language in SCRIPTS else "en"
    balance = get_balance(req.account_number)

    if balance is None:
        response_text = _get_script("balance_error", lang)
    else:
        response_text = _get_script("balance_response", lang, balance=f"{balance:,.2f}")

    audio_url = _generate_audio(response_text, lang)
    return BalanceResponse(balance=balance, response_text=response_text, audio_url=audio_url)


@app.post("/api/loan/apply", response_model=LoanApplyResponse)
async def apply_for_loan(req: LoanApplyRequest):
    lang = req.language if req.language in SCRIPTS else "en"
    result = apply_loan(req.amount, req.purpose)
    response_text = _get_script("loan_submitted", lang, id=result["application_id"])
    audio_url = _generate_audio(response_text, lang)
    return LoanApplyResponse(
        application_id=result["application_id"],
        status=result["status"],
        response_text=response_text,
        audio_url=audio_url,
    )


@app.post("/api/branch/nearby", response_model=BranchResponse)
async def find_branch(req: BranchRequest):
    lang = req.language if req.language in SCRIPTS else "en"
    branches = get_nearby_branches(req.location, lang)

    if not branches:
        response_text = _get_script("branch_not_found", lang)
    else:
        b = branches[0]
        response_text = _get_script("branch_response", lang, name=b["name"], address=b["address"], distance=b["distance"])

    audio_url = _generate_audio(response_text, lang)
    return BranchResponse(
        branches=branches[:3],
        response_text=response_text,
        audio_url=audio_url,
    )


@app.get("/api/audio/{audio_id}")
async def get_audio(audio_id: str):
    audio_bytes = SESSION_STORE.get(f"audio_{audio_id}")
    if audio_bytes is None:
        raise HTTPException(status_code=404, detail="Audio not found or expired")
    return Response(content=audio_bytes, media_type=AUDIO_CONTENT_TYPE)


@app.get("/api/compliance/rules")
async def get_compliance_rules():
    rules_list = [
        {"id": r["id"], "title": r["title"], "severity": r["severity"], "description": r["description"], "wcag_ref": r["wcag_ref"]}
        for r in IS_17802_RULES.values()
    ]
    return ComplianceResponse(
        standard="IS 17802 (Indian Standard on Accessibility)",
        total_rules=len(rules_list),
        rules=rules_list,
    )


@app.get("/api/compliance/check")
async def check_compliance():
    sample_html = """
    <!DOCTYPE html><html lang="hi">
    <head><title>OSAM Banking</title></head>
    <body>
    <button aria-label="बैलेंस चेक करें">1</button>
    <img src="logo.png" alt="OSAM लोगो" />
    </body>
    </html>
    """
    report = generate_accessibility_report(sample_html)
    return report


@app.post("/api/compliance/audit")
async def compliance_audit(req: ComplianceAuditRequest):
    try:
        report = await audit_url(req.url)
        return report
    except httpx.HTTPError as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audit failed: {str(e)}")


@app.post("/api/voice/upload")
async def upload_audio(file: UploadFile = File(...), language: str = Form("hi")):
    audio_bytes = await file.read()
    transcript = transcribe(audio_bytes, language)
    lang = language if language in SCRIPTS else "en"
    intent = detect_intent(transcript, lang)

    return {
        "filename": file.filename,
        "transcript": transcript,
        "intent": intent,
        "language": lang,
    }


WEB_UI_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "web", "public", "index.html")


@app.get("/", include_in_schema=False)
@app.get("/app", include_in_schema=False)
async def serve_web_ui():
    if os.path.isfile(WEB_UI_PATH):
        return HTMLResponse(open(WEB_UI_PATH, encoding="utf-8").read())
    return HTMLResponse("<h1>OSAM Voice Banking</h1><p>Web UI not found. Run the backend server.</p>")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8002"))
    uvicorn.run(app, host="0.0.0.0", port=port)
