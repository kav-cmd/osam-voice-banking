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
        {"name": "IPPB दिल्ली मुख्य शाखा", "address": "स्पीड पोस्ट सेंटर, मार्केट रोड, नई दिल्ली", "distance": 1.2, "timings": "सुबह 9 बजे से शाम 5 बजे तक"},
        {"name": "IPPB करोल बाग शाखा", "address": "करोल बाग, नई दिल्ली", "distance": 3.5, "timings": "सुबह 9 बजे से शाम 5 बजे तक"},
    ],
    "mumbai": [
        {"name": "IPPB मुंबई मुख्य शाखा", "address": "जीपीओ, मुंबई", "distance": 0.8, "timings": "सुबह 9.30 बजे से शाम 4.30 बजे तक"},
    ],
    "chennai": [
        {"name": "IPPB चेन्नई शाखा", "address": "अन्ना सालाई, चेन्नई", "distance": 2.1, "timings": "सुबह 9 बजे से शाम 5 बजे तक"},
    ],
    "kolkata": [
        {"name": "IPPB कोलकाता शाखा", "address": "कोलकाता जीपीओ, पश्चिम बंगाल", "distance": 1.5, "timings": "सुबह 9 बजे से शाम 4 बजे तक"},
    ],
    "bangalore": [
        {"name": "IPPB बेंगलुरु शाखा", "address": "महात्मा गांधी रोड, बेंगलुरु", "distance": 1.8, "timings": "सुबह 9.30 बजे से शाम 4.30 बजे तक"},
    ],
    "lucknow": [
        {"name": "IPPB लखनऊ शाखा", "address": "डाक भवन, लखनऊ", "distance": 0.5, "timings": "सुबह 9 बजे से शाम 5 बजे तक"},
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
        return MOCK_BRANCHES[city_key]

    return []
