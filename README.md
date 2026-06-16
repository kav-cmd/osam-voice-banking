# OSAM — Voice Banking for India

> **O**pen **S**ource **A**ccessible **M**obile Banking  
> Reserve Bank Innovation Hub (RBIH) — Confidential Working Paper

OSAM is a voice-enabled banking system that integrates with IPPB (India Post Payments Bank) to provide accessible banking in Hindi, Tamil, and English. Built for users who cannot read or see — voice is the interface.

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

API docs at http://localhost:8002/docs

### Web Frontend

```bash
cd web
npm install
npm start
```

Opens at http://localhost:3000

### Mobile (Flutter)

```bash
cd mobile
flutter pub get
flutter run
```

## Voice Commands

| Command | Hindi | Tamil | English |
|---------|-------|-------|---------|
| Check Balance | "मेरा बैलेंस चेक करें" | "என் இருப்பைச் சரிபார்" | "check my balance" |
| Apply for Loan | "लोन के लिए आवेदन करें" | "கடனுக்கு விண்ணப்பி" | "apply for a loan" |
| Find Branch | "निकटतम शाखा खोजें" | "அருகிலுள்ள கிளையைக் கண்டுபிடி" | "find nearest branch" |

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend API | FastAPI (Python) |
| Voice ASR | IndicConformer (600M multilingual) |
| TTS | gTTS / Flutter TTS |
| Web UI | React + TypeScript |
| Mobile | Flutter (with haptic feedback) |
| Accessibility | axe-core + IS 17802 rules |
| Documentation | Docusaurus + OpenAPI 3.0 |
| Deployment | Render / GovCloud |

## Project Structure

```
osam/
├── backend/          # FastAPI server
│   ├── app/
│   │   ├── main.py           # API routes
│   │   ├── scripts.py         # Hindi/Tamil/English scripts
│   │   ├── intent.py          # Intent parser
│   │   ├── ippb_mock.py       # Mock IPPB API
│   │   ├── voice.py           # ASR integration
│   │   ├── tts.py             # Text-to-Speech
│   │   └── compliance.py      # IS 17802 rules
│   ├── audio/                 # Cached TTS audio
│   └── requirements.txt
├── web/               # React frontend
├── mobile/            # Flutter app
├── docs/              # Docusaurus + OpenAPI
└── README.md
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/languages` | Supported languages |
| GET | `/api/scripts/{lang}` | Voice scripts |
| POST | `/api/voice/process` | Process voice command |
| POST | `/api/voice/upload` | Upload audio for ASR |
| POST | `/api/balance` | Check balance |
| POST | `/api/loan/apply` | Apply for loan |
| POST | `/api/branch/nearby` | Find nearest branch |
| GET | `/api/audio/{id}` | Get generated audio |
| GET | `/api/compliance/rules` | IS 17802 rules |
| GET | `/api/compliance/check` | Run compliance check |

## Accessibility

- **IS 17802** — Indian Standard on Accessibility
- **NVDA** — Windows screen reader tested
- **TalkBack** — Android screen reader tested
- **Haptic feedback** — 1 vibration (success), 2 vibrations (error)
- **Keyboard navigation** — All controls reachable via Tab/Enter
- **ARIA labels** — Every interactive element labeled
- **Contrast ratio** — Minimum 4.5:1 throughout

## Deployment

```bash
# 1. Push to GitHub
git init && git add . && git commit -m "Initial commit: OSAM Voice Banking"
git remote add origin https://github.com/kav-cmd/osam-voice-banking.git
git push -u origin main

# 2. Deploy on Render
# Connect repo → Select "Web Service"
# Root: backend/
# Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## IPPB Integration

OSAM uses a mock IPPB API for development. To connect to the real IPPB IVR system:

1. Contact IPPB for API credentials
2. Set `IPPB_API_KEY` and `IPPB_BASE_URL` environment variables
3. Update `ippb_mock.py` to call real endpoints

## License

MIT — Open source for public good under RBI Innovation Hub guidance.
