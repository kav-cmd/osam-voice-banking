---
sidebar_position: 1
---

# OSAM Voice Banking

**OSAM** (Open Source Accessible Mobile Banking) is a voice-enabled banking system that integrates with India Post Payments Bank (IPPB) to provide accessible banking in Hindi, Tamil, and English.

## Why OSAM?

- **1.6 lakh post offices** connected via IPPB
- **13 Indian languages** supported by IPPB's IVR
- **Voice is the interface** — no literacy, no vision required
- **Built for the 500M+ Indians** who have phones but limited access to digital banking

## Voice Commands

| Hindi | Tamil | English |
|-------|-------|---------|
| "मेरा बैलेंस चेक करें" | "என் இருப்பைச் சரிபார்" | "Check my balance" |
| "लोन के लिए आवेदन करें" | "கடனுக்கு விண்ணப்பி" | "Apply for a loan" |
| "निकटतम शाखा खोजें" | "அருகிலுள்ள கிளையைக் கண்டுபிடி" | "Find nearest branch" |

## How It Works

1. User calls IPPB IVR or opens the OSAM app
2. Speaks a voice command in Hindi or Tamil
3. OSAM transcribes (IndicConformer ASR) → detects intent → processes → responds
4. Response delivered via TTS audio in the same language
