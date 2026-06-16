import re

INTENT_KEYWORDS = {
    "hi": {
        "balance": [
            r"बैलेंस", r"शेष", r"पैसे", r"रुपये", r"खाता.*जानकारी",
            r"कितना.*पैसा", r"बचत", r"अकाउंट",
        ],
        "loan": [
            r"लोन", r"कर्ज", r"ऋण", r"उधार", r"किश्त",
        ],
        "branch": [
            r"शाखा", r"ब्रांच", r"बैंक", r"निकटतम", r"पास.*शाखा",
            r"कहाँ.*शाखा", r"लोकेशन",
        ],
        "help": [r"मदद", r"सहायता", r"क्या.*कर", r"कैसे"],
        "yes": [r"हाँ", r"हां", r"हैं", r"जी हाँ", r"ठीक", r"ह", r"1"],
        "no": [r"नहीं", r"ना", r"नहि", r"रद्द", r"2"],
    },
    "ta": {
        "balance": [
            r"இருப்பு", r"பேலன்ஸ்", r"கணக்கு", r"பணம்", r"ரூபாய்",
            r"எவ்வளவு.*பணம்", r"சேமிப்பு",
        ],
        "loan": [
            r"கடன்", r"லோன்", r"கடன்.*விண்ணப்ப", r"கடன்.*தொகை",
        ],
        "branch": [
            r"கிளை", r"கிளையை", r"வங்கி", r"அருகில்", r"இடம்",
            r"எங்கே.*கிளை",
        ],
        "help": [r"உதவி", r"என்ன.*செய்ய"],
        "yes": [r"ஆம்", r"சரி", r"சர", r"1"],
        "no": [r"இல்லை", r"வேண்டாம்", r"2"],
    },
    "en": {
        "balance": [
            r"balance", r"money", r"account.*info", r"how much",
            r"savings", r"bank.*balance", r"check.*balance",
        ],
        "loan": [
            r"loan", r"borrow", r"credit", r"emi", r"finance",
        ],
        "branch": [
            r"branch", r"nearest.*branch", r"bank.*near", r"location",
            r"where.*branch", r"find.*branch",
        ],
        "help": [r"help", r"what.*do", r"how.*use", r"guide"],
        "yes": [r"yes", r"yeah", r"yep", r"sure", r"okay", r"ok", r"1", r"correct"],
        "no": [r"no", r"nope", r"nah", r"cancel", r"2", r"not now"],
    },
}

TRANSFER_KEYWORDS = [r"transfer", r"send", r"भेज", r"ट्रांसफर", r"அனுப்ப"]
STOP_KEYWORDS = [r"stop", r"exit", r"quit", r"goodbye", r"bye", r"बंद", r"रुको", r"நிறுத்து"]


def detect_intent(text: str, lang: str = "en") -> str:
    if not text or not text.strip():
        return "unknown"

    text_lower = text.strip().lower()

    for kw in STOP_KEYWORDS:
        if re.search(kw, text_lower, re.IGNORECASE):
            return "goodbye"

    lang_keywords = INTENT_KEYWORDS.get(lang, INTENT_KEYWORDS["en"])

    for intent, patterns in lang_keywords.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return intent

    for kw in TRANSFER_KEYWORDS:
        if re.search(kw, text_lower, re.IGNORECASE):
            return "transfer"

    return "unknown"
