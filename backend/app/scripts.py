HINDI_SCRIPTS = {
    "welcome": (
        "OSAM वॉइस बैंकिंग में आपका स्वागत है। "
        "हिंदी के लिए 1 दबाएं। "
        "तमिल के लिए 2 दबाएं। "
        "अंग्रेज़ी के लिए 3 दबाएं।"
    ),
    "main_menu": (
        "खाता शेष जानने के लिए 1 दबाएं। "
        "लोन के लिए 2 दबाएं। "
        "नज़दीकी शाखा के लिए 3 दबाएं। "
        "फिर से सुनने के लिए 9 दबाएं।"
    ),
    "balance_prompt": "कृपया अपना 6 अंकों का खाता नंबर बोलें या डायल करें।",
    "balance_response": "आपके खाते में {balance} रुपये शेष हैं।",
    "balance_error": "खाता नंबर नहीं मिला। 1 सुनिश्चित करें कि नंबर 6 अंकों का है। 2 दोबारा प्रयास करें। मुख्य मेनू के लिए 0 दबाएं।",
    "loan_purpose_prompt": "लोन का कारण बताएं। जैसे: व्यापार, शिक्षा, या खेती।",
    "loan_amount_prompt": "कृपया लोन की रकम बताएं। जैसे: पचास हज़ार या दो लाख।",
    "loan_confirm": (
        "क्या आप {amount} रुपये लोन लेना चाहते हैं? "
        "हां के लिए 1 दबाएं। नहीं के लिए 2 दबाएं। "
        "अगर सही नहीं है तो मुख्य मेनू के लिए 0 दबाएं।"
    ),
    "loan_submitted": "आपका लोन आवेदन {id} जमा हो गया। हम 2 दिन में संपर्क करेंगे।",
    "loan_cancelled": "लोन रद्द किया गया। मुख्य मेनू के लिए 0 दबाएं।",
    "loan_processing": "आपका {amount} रुपये का लोन आवेदन {purpose} के लिए मिल गया है। कृपया प्रतीक्षा करें।",
    "branch_prompt_location": "अपने शहर या पिन कोड का नाम बताएं। जैसे: दिल्ली, मुंबई, या 110001।",
    "branch_response": "आपकी नज़दीकी शाखा {name} है। पता: {address}। दूरी {distance} किलोमीटर।",
    "branch_not_found": "इस शहर में कोई शाखा नहीं मिली। दूसरा शहर बताएं। मुख्य मेनू के लिए 0 दबाएं।",
    "goodbye": "OSAM वॉइस बैंकिंग का उपयोग करने के लिए धन्यवाद। नमस्ते।",
    "error": (
        "समझ नहीं आया। कृपया फिर से कहें। "
        "खाता शेष के लिए 1। लोन के लिए 2। शाखा के लिए 3। "
        "मुख्य मेनू के लिए 0।"
    ),
    "help": "आप कह सकते हैं: बैलेंस चेक करें, लोन चाहिए, या शाखा खोजें। या फिर 1, 2, 3 दबाएं।",
    "ivr_greeting": "नमस्कार। यह OSAM बैंकिंग सेवा है। आगे बढ़ने के लिए कोई भी बटन दबाएं।",
    "waiting": "कृपया प्रतीक्षा करें। आपका अनुरोध प्रोसेस हो रहा है।",
    "repeat_menu": "फिर से सुनें: खाता शेष के लिए 1, लोन के लिए 2, शाखा के लिए 3।",
}

TAMIL_SCRIPTS = {
    "welcome": (
        "OSAM குரல் வங்கிக்கு வரவேற்கிறோம். "
        "இந்திக்கு 1ஐ அழுத்தவும். "
        "தமிழுக்கு 2ஐ அழுத்தவும். "
        "ஆங்கிலத்திற்கு 3ஐ அழுத்தவும்."
    ),
    "main_menu": (
        "கணக்கு இருப்புத் தெரிய 1ஐ அழுத்தவும். "
        "கடனுக்கு 2ஐ அழுத்தவும். "
        "அருகில் உள்ள கிளைக்கு 3ஐ அழுத்தவும். "
        "மீண்டும் கேட்க 9ஐ அழுத்தவும்."
    ),
    "balance_prompt": "உங்கள் 6 இலக்க கணக்கு எண்ணைச் சொல்லுங்கள் அல்லது டயல் செய்யுங்கள்.",
    "balance_response": "உங்கள் கணக்கில் {balance} ரூபாய் உள்ளது.",
    "balance_error": "கணக்கு எண் கிடைக்கவில்லை. சரியான 6 இலக்க எண்ணை உள்ளிடவும். மீண்டும் 0 அழுத்தவும்.",
    "loan_purpose_prompt": "கடனுக்கான காரணத்தைச் சொல்லுங்கள். உதாரணம்: வியாபாரம், கல்வி, அல்லது விவசாயம்.",
    "loan_amount_prompt": "கடன் தொகையைச் சொல்லுங்கள். உதாரணம்: ஐம்பதாயிரம் அல்லது இரண்டு லட்சம்.",
    "loan_confirm": (
        "நீங்கள் {amount} ரூபாய் கடன் வாங்க விரும்புகிறீர்களா? "
        "ஆம் எனில் 1ஐ அழுத்தவும். இல்லை எனில் 2ஐ அழுத்தவும். "
        "முதல் பக்கத்திற்கு 0 அழுத்தவும்."
    ),
    "loan_submitted": "உங்கள் கடன் விண்ணப்பம் {id} சமர்ப்பிக்கப்பட்டது. 2 நாட்களில் தொடர்புகொள்வோம்.",
    "loan_cancelled": "கடன் ரத்து செய்யப்பட்டது. முதல் பக்கத்திற்கு 0 அழுத்தவும்.",
    "loan_processing": "உங்கள் {amount} ரூபாய் கடன் விண்ணப்பம் {purpose}க்காகப் பெறப்பட்டது. தயவுசெய்து காத்திருங்கள்.",
    "branch_prompt_location": "உங்கள் நகரம் அல்லது பின் குறியீட்டைச் சொல்லுங்கள். உதாரணம்: சென்னை, மும்பை, அல்லது 600001.",
    "branch_response": "உங்கள் அருகில் உள்ள கிளை {name}. முகவரி: {address}. தூரம் {distance} கிலோமீட்டர்.",
    "branch_not_found": "இந்த நகரத்தில் கிளை இல்லை. வேறு நகரத்தைச் சொல்லுங்கள். முதல் பக்கத்திற்கு 0 அழுத்தவும்.",
    "goodbye": "OSAM குரல் வங்கியைப் பயன்படுத்தியதற்கு நன்றி. வணக்கம்.",
    "error": (
        "புரியவில்லை. மீண்டும் சொல்லுங்கள். "
        "கணக்கு இருப்புக்கு 1. கடனுக்கு 2. கிளைக்கு 3. "
        "முதல் பக்கத்திற்கு 0."
    ),
    "help": "நீங்கள் சொல்லலாம்: இருப்பைச் சரிபார், கடன் வேண்டும், அல்லது கிளையைத் தேடு. அல்லது 1, 2, 3 அழுத்தவும்.",
    "ivr_greeting": "வணக்கம். இது OSAM வங்கி சேவை. தொடர எந்தப் பொத்தானையும் அழுத்தவும்.",
    "waiting": "தயவுசெய்து காத்திருங்கள். உங்கள் கோரிக்கை செயலாக்கப்படுகிறது.",
    "repeat_menu": "மீண்டும் கேட்க: கணக்கு இருப்புக்கு 1, கடனுக்கு 2, கிளைக்கு 3.",
}

ENGLISH_SCRIPTS = {
    "welcome": "Welcome to OSAM Voice Banking. Press 1 for Hindi, 2 for Tamil, or 3 for English.",
    "main_menu": "Press 1 for balance. Press 2 for loan. Press 3 for nearest branch. Press 9 to repeat.",
    "balance_prompt": "Please say or dial your 6-digit account number.",
    "balance_response": "Your account balance is {balance} rupees.",
    "balance_error": "Account not found. Make sure it is 6 digits. Try again or press 0 for menu.",
    "loan_purpose_prompt": "Tell the reason for the loan. Example: business, education, or farming.",
    "loan_amount_prompt": "Tell the loan amount. Example: fifty thousand or two lakh.",
    "loan_confirm": "Do you want a loan of {amount} rupees? Press 1 for yes. Press 2 for no. Press 0 for menu.",
    "loan_submitted": "Your loan application {id} is submitted. We will contact you in 2 days.",
    "loan_cancelled": "Loan cancelled. Press 0 for main menu.",
    "loan_processing": "Your loan of {amount} rupees for {purpose} is being processed. Please wait.",
    "branch_prompt_location": "Tell your city or pin code. Example: Delhi, Mumbai, or 110001.",
    "branch_response": "Your nearest branch is {name}. Address: {address}. Distance: {distance} kilometers.",
    "branch_not_found": "No branch in this city. Try another city. Press 0 for main menu.",
    "goodbye": "Thank you for using OSAM Voice Banking. Goodbye.",
    "error": "Did not understand. Say again. Press 1 for balance. 2 for loan. 3 for branch. 0 for menu.",
    "help": "You can say: check balance, need loan, or find branch. Or press 1, 2, or 3.",
    "ivr_greeting": "Hello. This is OSAM Banking Service. Press any key to continue.",
    "waiting": "Please wait. Processing your request.",
    "repeat_menu": "Repeat: press 1 for balance, 2 for loan, 3 for branch.",
}

SCRIPTS = {
    "hi": HINDI_SCRIPTS,
    "ta": TAMIL_SCRIPTS,
    "en": ENGLISH_SCRIPTS,
}

LANGUAGE_NAMES = {"hi": "हिन्दी", "ta": "தமிழ்", "en": "English"}
