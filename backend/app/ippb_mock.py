import uuid
import random
from typing import Optional

MOCK_BALANCES = {
    "123456": 15250.75,
    "789012": 48200.00,
    "345678": 8100.50,
    "901234": 125000.00,
    "567890": 3250.00,
}

MOCK_BRANCHES = {
    "delhi": [
        {"name": {"hi": "IPPB दिल्ली मुख्य शाखा", "ta": "IPPB டெல்லி முதன்மை கிளை", "en": "IPPB Delhi Main Branch"}, "address": {"hi": "स्पीड पोस्ट सेंटर, मार्केट रोड, नई दिल्ली", "ta": "ஸ்பீட் போஸ்ட் சென்டர், மார்க்கெட் ரோடு, புது டெல்லி", "en": "Speed Post Centre, Market Road, New Delhi"}, "distance": 1.2, "timings": {"hi": "सुबह 9 बजे से शाम 5 बजे तक", "ta": "காலை 9 மணி முதல் மாலை 5 மணி வரை", "en": "9 AM to 5 PM"}},
        {"name": {"hi": "IPPB करोल बाग शाखा", "ta": "IPPB கரோல் பாக் கிளை", "en": "IPPB Karol Bagh Branch"}, "address": {"hi": "करोल बाग, नई दिल्ली", "ta": "கரோல் பாக், புது டெல்லி", "en": "Karol Bagh, New Delhi"}, "distance": 3.5, "timings": {"hi": "सुबह 9 बजे से शाम 5 बजे तक", "ta": "காலை 9 மணி முதல் மாலை 5 மணி வரை", "en": "9 AM to 5 PM"}},
    ],
    "mumbai": [
        {"name": {"hi": "IPPB मुंबई मुख्य शाखा", "ta": "IPPB மும்பை முதன்மை கிளை", "en": "IPPB Mumbai Main Branch"}, "address": {"hi": "जीपीओ, मुंबई", "ta": "ஜிபிஓ, மும்பை", "en": "GPO, Mumbai"}, "distance": 0.8, "timings": {"hi": "सुबह 9.30 बजे से शाम 4.30 बजे तक", "ta": "காலை 9.30 மணி முதல் மாலை 4.30 மணி வரை", "en": "9:30 AM to 4:30 PM"}},
    ],
    "chennai": [
        {"name": {"hi": "IPPB चेन्नई शाखा", "ta": "IPPB சென்னை கிளை", "en": "IPPB Chennai Branch"}, "address": {"hi": "अन्ना सालाई, चेन्नई", "ta": "அண்ணா சாலை, சென்னை", "en": "Anna Salai, Chennai"}, "distance": 2.1, "timings": {"hi": "सुबह 9 बजे से शाम 5 बजे तक", "ta": "காலை 9 மணி முதல் மாலை 5 மணி வரை", "en": "9 AM to 5 PM"}},
    ],
    "kolkata": [
        {"name": {"hi": "IPPB कोलकाता शाखा", "ta": "IPPB கொல்கத்தா கிளை", "en": "IPPB Kolkata Branch"}, "address": {"hi": "कोलकाता जीपीओ, पश्चिम बंगाल", "ta": "கொல்கத்தா ஜிபிஓ, மேற்கு வங்காளம்", "en": "Kolkata GPO, West Bengal"}, "distance": 1.5, "timings": {"hi": "सुबह 9 बजे से शाम 4 बजे तक", "ta": "காலை 9 மணி முதல் மாலை 4 மணி வரை", "en": "9 AM to 4 PM"}},
    ],
    "bangalore": [
        {"name": {"hi": "IPPB बेंगलुरु शाखा", "ta": "IPPB பெங்களூரு கிளை", "en": "IPPB Bangalore Branch"}, "address": {"hi": "महात्मा गांधी रोड, बेंगलुरु", "ta": "மகாத்மா காந்தி சாலை, பெங்களூரு", "en": "MG Road, Bangalore"}, "distance": 1.8, "timings": {"hi": "सुबह 9.30 बजे से शाम 4.30 बजे तक", "ta": "காலை 9.30 மணி முதல் மாலை 4.30 மணி வரை", "en": "9:30 AM to 4:30 PM"}},
    ],
    "lucknow": [
        {"name": {"hi": "IPPB लखनऊ शाखा", "ta": "IPPB லக்னோ கிளை", "en": "IPPB Lucknow Branch"}, "address": {"hi": "डाक भवन, लखनऊ", "ta": "அஞ்சல் பவன், லக்னோ", "en": "Dak Bhawan, Lucknow"}, "distance": 0.5, "timings": {"hi": "सुबह 9 बजे से शाम 5 बजे तक", "ta": "காலை 9 மணி முதல் மாலை 5 மணி வரை", "en": "9 AM to 5 PM"}},
    ],
}

BRANCH_ALIASES = {
    "hi": {
        r"दिल्ली|नई दिल्ली": "delhi",
        r"मुंबई|बॉम्बे": "mumbai",
        r"चेन्नई|मद्रास": "chennai",
        r"कोलकाता|कलकत्ता": "kolkata",
        r"बेंगलुरु|बंगलौर": "bangalore",
        r"लखनऊ": "lucknow",
    },
    "ta": {
        r"சென்னை|மதராஸ்": "chennai",
        r"டெல்லி": "delhi",
        r"மும்பை": "mumbai",
        r"கொல்கத்தா": "kolkata",
        r"பெங்களூரு": "bangalore",
    },
    "en": {
        r"delhi|new delhi": "delhi",
        r"mumbai|bombay": "mumbai",
        r"chennai|madras": "chennai",
        r"kolkata|calcutta": "kolkata",
        r"bangalore|bengaluru": "bangalore",
        r"lucknow": "lucknow",
    },
}


def get_balance(account_number: str) -> Optional[float]:
    return MOCK_BALANCES.get(account_number.strip())


def apply_loan(amount: float, purpose: str) -> dict:
    loan_id = f"OSAM-{uuid.uuid4().hex[:8].upper()}"
    return {
        "application_id": loan_id,
        "amount": amount,
        "purpose": purpose,
        "status": "submitted",
        "message": f"Loan application {loan_id} submitted for ₹{amount:,.2f} for {purpose}.",
    }


def get_nearby_branches(location: str, lang: str = "en") -> list[dict]:
    location_lower = location.strip().lower()
    city_key = None

    aliases = BRANCH_ALIASES.get(lang, BRANCH_ALIASES["en"])
    for pattern, city in aliases.items():
        import re
        if re.search(pattern, location, re.IGNORECASE):
            city_key = city
            break

    if not city_key:
        location_lower_norm = location_lower.replace(" ", "")
        for known_city in MOCK_BRANCHES:
            if known_city in location_lower or location_lower_norm == known_city.replace(" ", ""):
                city_key = known_city
                break

    if not city_key:
        for city, city_branches in MOCK_BRANCHES.items():
            for alias_list in BRANCH_ALIASES.get(lang, BRANCH_ALIASES["en"]).values():
                if city == alias_list:
                    city_key = city
                    break

    if city_key and city_key in MOCK_BRANCHES:
        results = []
        for b in MOCK_BRANCHES[city_key]:
            results.append({
                "name": b["name"].get(lang, b["name"].get("en", "")),
                "address": b["address"].get(lang, b["address"].get("en", "")),
                "distance": b["distance"],
                "timings": b["timings"].get(lang, b["timings"].get("en", "")),
            })
        return results

    return []
