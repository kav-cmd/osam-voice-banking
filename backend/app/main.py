import os
import uuid
import logging
import re
from contextlib import asynccontextmanager
from typing import Optional
from datetime import datetime

import httpx
from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response, HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, field_validator
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from .scripts import SCRIPTS, LANGUAGE_NAMES
from .intent import detect_intent
from .ippb_mock import get_balance, get_nearby_branches
from .voice import transcribe, load_asr
from .tts import text_to_speech
from .compliance import generate_accessibility_report, IS_17802_RULES, audit_url
from .database import init_db, get_session
from .models import User, LoanApplication, Transaction
from .auth import hash_password, verify_password, create_access_token, get_current_user, get_admin_user
from .encryption import hash_pan, hash_email, encrypt_phone, decrypt_phone
from .rate_limit import RateLimitMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AUDIO_CONTENT_TYPE = "audio/mpeg"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting OSAM Voice Banking Server...")
    load_asr()
    await init_db()
    yield
    logger.info("Shutting down OSAM Voice Banking Server...")


app = FastAPI(
    title="OSAM Voice Banking API",
    description="Voice-enabled banking system for IPPB integration — Hindi, Tamil, English",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(RateLimitMiddleware, max_requests=60, window_seconds=60)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


PAN_REGEX = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")
PHONE_REGEX = re.compile(r"^[6-9][0-9]{9}$")
EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


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
    name: str = ""
    pan: str = ""
    phone: str = ""
    email: str = ""
    dob: str = ""
    income: float = 0
    existing_emi: float = 0
    amount: float = 500000
    tenure: int = 36
    employment: str = "salaried"
    company: str = ""
    docs: str = ""
    purpose: str = "Personal Loan from OSAM Portal"
    language: str = "hi"

    @field_validator("pan")
    @classmethod
    def validate_pan(cls, v):
        if v and not PAN_REGEX.match(v.strip().upper()):
            raise ValueError("Invalid PAN format (expected: ABCDE1234F)")
        return v.strip().upper()

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if v and not PHONE_REGEX.match(v.strip()):
            raise ValueError("Invalid phone number (expected: 10-digit Indian mobile)")
        return v.strip()

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if v and not EMAIL_REGEX.match(v.strip()):
            raise ValueError("Invalid email address")
        return v.strip().lower()


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


class AuthRegisterRequest(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("Username must be at least 3 characters")
        return v.strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v


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
    return {"status": "ok", "service": "OSAM Voice Banking", "version": "2.0.0"}


@app.get("/api/languages")
async def list_languages():
    return {"languages": [{"code": k, "name": v} for k, v in LANGUAGE_NAMES.items()]}


@app.get("/api/scripts/{language}")
async def get_scripts(language: str):
    if language not in SCRIPTS:
        raise HTTPException(status_code=404, detail=f"Language '{language}' not supported")
    return ScriptsResponse(language=language, scripts=SCRIPTS[language])


# ─── Auth ────────────────────────────────────────────────────────────────────

@app.post("/api/auth/register")
async def register(req: AuthRegisterRequest, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.username == req.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(username=req.username, password_hash=hash_password(req.password), role="user")
    session.add(user)
    await session.commit()
    await session.refresh(user)
    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer", "username": user.username, "role": user.role}


@app.post("/api/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer", "username": user.username, "role": user.role}


@app.get("/api/auth/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "role": current_user.role, "created_at": str(current_user.created_at)}


# ─── Dashboard ───────────────────────────────────────────────────────────────

@app.get("/api/dashboard")
async def get_dashboard(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    apps_result = await session.execute(
        select(LoanApplication).where(LoanApplication.user_id == current_user.id).order_by(desc(LoanApplication.created_at)).limit(5)
    )
    applications = []
    for a in apps_result.scalars().all():
        applications.append({
            "application_id": a.application_id, "amount": a.amount,
            "status": a.status, "created_at": str(a.created_at),
        })
    txn_result = await session.execute(
        select(Transaction).where(Transaction.user_id == current_user.id).order_by(desc(Transaction.created_at)).limit(5)
    )
    transactions_list = []
    for t in txn_result.scalars().all():
        transactions_list.append({
            "id": t.id, "txn_type": t.txn_type, "amount": t.amount,
            "description": t.description, "balance_after": t.balance_after,
            "created_at": str(t.created_at),
        })
    return {
        "username": current_user.username,
        "applications_count": len(applications),
        "recent_applications": applications,
        "recent_transactions": transactions_list,
    }


# ─── Voice ───────────────────────────────────────────────────────────────────

@app.post("/api/voice/process", response_model=ProcessVoiceResponse)
async def process_voice(req: ProcessVoiceRequest):
    lang = req.language if req.language in SCRIPTS else "en"
    session_id = req.session_id or uuid.uuid4().hex
    transcript = req.text or ""
    if req.audio and not transcript:
        transcript = "voice command received"
    intent = detect_intent(transcript, lang)
    SESSION_STORE[session_id] = {"intent": intent, "language": lang, "step": intent}
    response_text = _get_script("help", lang)
    requires_input = True
    if intent == "balance":
        response_text = _get_script("balance_prompt", lang)
    elif intent == "loan":
        response_text = _get_script("loan_purpose_prompt", lang)
    elif intent == "branch":
        response_text = _get_script("branch_prompt_location", lang)
    elif intent == "goodbye":
        response_text = _get_script("goodbye", lang)
        requires_input = False
    elif intent == "help" or intent == "unknown":
        response_text = _get_script("help", lang) + " " + _get_script("main_menu", lang)
    audio_url = _generate_audio(response_text, lang)
    return ProcessVoiceResponse(intent=intent, transcript=transcript, response_text=response_text, requires_input=requires_input, session_id=session_id, audio_url=audio_url)


@app.post("/api/voice/upload")
async def upload_audio(file: UploadFile = File(...), language: str = Form("hi")):
    audio_bytes = await file.read()
    transcript = transcribe(audio_bytes, language)
    lang = language if language in SCRIPTS else "en"
    intent = detect_intent(transcript, lang)
    return {"filename": file.filename, "transcript": transcript, "intent": intent, "language": lang}


# ─── Balance ─────────────────────────────────────────────────────────────────

@app.post("/api/balance", response_model=BalanceResponse)
async def check_balance(req: BalanceRequest):
    lang = req.language if req.language in SCRIPTS else "en"
    balance = get_balance(req.account_number)
    response_text = _get_script("balance_response", lang, balance=f"{balance:,.2f}") if balance is not None else _get_script("balance_error", lang)
    audio_url = _generate_audio(response_text, lang)
    return BalanceResponse(balance=balance, response_text=response_text, audio_url=audio_url)


async def get_current_user_if_token(authorization: Optional[str] = Header(None)):
    """Return user if valid token, None otherwise (no 401)."""
    if not authorization:
        return None
    from .auth import decode_token
    payload = decode_token(authorization.replace("Bearer ", ""))
    if payload is None:
        return None
    async with async_session() as session:
        result = await session.execute(select(User).where(User.username == payload["sub"]))
        return result.scalar_one_or_none()


# ─── Loan Applications ───────────────────────────────────────────────────────

@app.post("/api/loan/apply", response_model=LoanApplyResponse)
async def apply_for_loan(
    req: LoanApplyRequest,
    session: AsyncSession = Depends(get_session),
    current_user: Optional[User] = Depends(get_current_user_if_token),
):
    lang = req.language if req.language in SCRIPTS else "en"
    app_id = f"OSAM-{uuid.uuid4().hex[:8].upper()}"
    record = LoanApplication(
        user_id=current_user.id if current_user else None,
        application_id=app_id,
        name=req.name,
        pan_hash=hash_pan(req.pan),
        phone_encrypted=encrypt_phone(req.phone),
        email_hash=hash_email(req.email),
        dob=req.dob,
        income=req.income,
        existing_emi=req.existing_emi,
        amount=req.amount,
        tenure=req.tenure,
        employment=req.employment,
        company=req.company,
        docs=req.docs,
        purpose=req.purpose,
        status="submitted",
    )
    session.add(record)
    # Record a mock transaction for the loan amount
    if req.amount > 0:
        txn = Transaction(
            user_id=current_user.id if current_user else None,
            account_number="LOAN-DISB",
            txn_type="credit",
            amount=req.amount,
            description=f"Loan disbursal {app_id}",
            balance_after=req.amount,
        )
        session.add(txn)
    await session.commit()
    await session.refresh(record)
    response_text = _get_script("loan_submitted", lang, id=app_id)
    audio_url = _generate_audio(response_text, lang)
    return LoanApplyResponse(application_id=app_id, status="submitted", response_text=response_text, audio_url=audio_url)


@app.get("/api/loan/applications")
async def list_my_applications(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    result = await session.execute(
        select(LoanApplication).where(LoanApplication.user_id == current_user.id).order_by(desc(LoanApplication.created_at))
    )
    apps = []
    for a in result.scalars().all():
        apps.append({
            "application_id": a.application_id, "name": a.name,
            "amount": a.amount, "status": a.status,
            "created_at": str(a.created_at),
        })
    return {"applications": apps}


# ─── Transactions ────────────────────────────────────────────────────────────

@app.get("/api/transactions")
async def get_transactions(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    result = await session.execute(
        select(Transaction).where(Transaction.user_id == current_user.id).order_by(desc(Transaction.created_at)).limit(20)
    )
    txns = []
    for t in result.scalars().all():
        txns.append({
            "id": t.id, "account_number": t.account_number,
            "txn_type": t.txn_type, "amount": t.amount,
            "description": t.description, "balance_after": t.balance_after,
            "created_at": str(t.created_at),
        })
    return {"transactions": txns}


# ─── Branch ──────────────────────────────────────────────────────────────────

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
    return BranchResponse(branches=branches[:3], response_text=response_text, audio_url=audio_url)


# ─── Audio ───────────────────────────────────────────────────────────────────

@app.get("/api/audio/{audio_id}")
async def get_audio(audio_id: str):
    audio_bytes = SESSION_STORE.get(f"audio_{audio_id}")
    if audio_bytes is None:
        raise HTTPException(status_code=404, detail="Audio not found or expired")
    return Response(content=audio_bytes, media_type=AUDIO_CONTENT_TYPE)


# ─── Compliance ──────────────────────────────────────────────────────────────

@app.get("/api/compliance/rules")
async def get_compliance_rules():
    rules_list = [
        {"id": r["id"], "title": r["title"], "severity": r["severity"], "description": r["description"], "wcag_ref": r["wcag_ref"]}
        for r in IS_17802_RULES.values()
    ]
    return ComplianceResponse(standard="IS 17802 (Indian Standard on Accessibility)", total_rules=len(rules_list), rules=rules_list)


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
    return generate_accessibility_report(sample_html)


@app.post("/api/compliance/audit")
async def compliance_audit(req: ComplianceAuditRequest):
    try:
        return await audit_url(req.url)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audit failed: {str(e)}")


# ─── Admin ───────────────────────────────────────────────────────────────────

@app.get("/api/admin/applications")
async def admin_list_applications(
    session: AsyncSession = Depends(get_session),
    admin: User = Depends(get_admin_user),
):
    result = await session.execute(
        select(LoanApplication).order_by(desc(LoanApplication.created_at)).limit(50)
    )
    apps = []
    for a in result.scalars().all():
        apps.append({
            "application_id": a.application_id, "name": a.name,
            "amount": a.amount, "status": a.status,
            "income": a.income, "employment": a.employment,
            "created_at": str(a.created_at),
        })
    return {"total": len(apps), "applications": apps}


@app.get("/api/admin/users")
async def admin_list_users(
    session: AsyncSession = Depends(get_session),
    admin: User = Depends(get_admin_user),
):
    result = await session.execute(select(User).order_by(User.id))
    users_list = []
    for u in result.scalars().all():
        users_list.append({"id": u.id, "username": u.username, "role": u.role, "created_at": str(u.created_at)})
    return {"users": users_list}


@app.patch("/api/admin/applications/{app_id}/status")
async def admin_update_status(
    app_id: str,
    status: str,
    session: AsyncSession = Depends(get_session),
    admin: User = Depends(get_admin_user),
):
    result = await session.execute(select(LoanApplication).where(LoanApplication.application_id == app_id))
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    if status not in ("submitted", "approved", "rejected"):
        raise HTTPException(status_code=400, detail="Invalid status")
    app.status = status
    await session.commit()
    return {"application_id": app_id, "status": status}


# ─── Web UI ──────────────────────────────────────────────────────────────────

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
