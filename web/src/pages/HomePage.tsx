import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import AccessibleButton from '../components/AccessibleButton';

export default function HomePage() {
  const [language, setLanguage] = useState('hi');

  const langOptions = [
    { code: 'hi', name: 'हिन्दी', nameEn: 'Hindi' },
    { code: 'ta', name: 'தமிழ்', nameEn: 'Tamil' },
    { code: 'en', name: 'English', nameEn: 'English' },
  ];

  return (
    <div className="page home-page">
      <section className="hero" aria-labelledby="hero-title">
        <h1 id="hero-title" lang={language}>
          {language === 'hi' ? 'OSAM वॉइस बैंकिंग में आपका स्वागत है' :
           language === 'ta' ? 'OSAM குரல் வங்கிக்கு வரவேற்கிறோம்' :
           'Welcome to OSAM Voice Banking'}
        </h1>
        <p className="hero-subtitle" lang={language}>
          {language === 'hi' ? 'IPPB के साथ हिंदी और तमिल में वॉइस बैंकिंग — बस बोलें, हम संभाल लेंगे।' :
           language === 'ta' ? 'IPPB உடன் இந்தி மற்றும் தமிழில் குரல் வங்கி — நீங்கள் பேசுங்கள், நாங்கள் கவனிப்போம்.' :
           'Voice banking in Hindi and Tamil with IPPB — just speak, we handle the rest.'}
        </p>

        <div className="language-selector" role="radiogroup" aria-label="भाषा चुनें">
          {langOptions.map((l) => (
            <button
              key={l.code}
              onClick={() => setLanguage(l.code)}
              className={`lang-btn ${language === l.code ? 'active' : ''}`}
              role="radio"
              aria-checked={language === l.code}
              lang={l.code}
            >
              {l.name}
              <span className="lang-sub">{l.nameEn}</span>
            </button>
          ))}
        </div>
      </section>

      <section className="features" aria-label="सुविधाएँ">
        <div className="feature-card">
          <span className="feature-icon" aria-hidden="true">💰</span>
          <h2 lang={language}>
            {language === 'hi' ? 'बैलेंस चेक करें' :
             language === 'ta' ? 'இருப்பைச் சரிபார்' :
             'Check Balance'}
          </h2>
          <p lang={language}>
            {language === 'hi' ? 'अपने खाते का शेष जानने के लिए बस "मेरा बैलेंस चेक करें" बोलें।' :
             language === 'ta' ? 'உங்கள் கணக்கு இருப்பை அறிய "என் இருப்பைச் சரிபார்" என்று சொல்லுங்கள்.' :
             'Just say "check my balance" to know your account balance.'}
          </p>
        </div>
        <div className="feature-card">
          <span className="feature-icon" aria-hidden="true">📋</span>
          <h2 lang={language}>
            {language === 'hi' ? 'लोन के लिए आवेदन' :
             language === 'ta' ? 'கடனுக்கு விண்ணப்பிக்க' :
             'Apply for Loan'}
          </h2>
          <p lang={language}>
            {language === 'hi' ? '"लोन के लिए आवेदन करें" बोलकर लोन आवेदन शुरू करें।' :
             language === 'ta' ? '"கடனுக்கு விண்ணப்பிக்க" என்று சொல்லி கடன் விண்ணப்பத்தைத் தொடங்குங்கள்.' :
             'Say "apply for a loan" to start your loan application process.'}
          </p>
        </div>
        <div className="feature-card">
          <span className="feature-icon" aria-hidden="true">📍</span>
          <h2 lang={language}>
            {language === 'hi' ? 'निकटतम शाखा खोजें' :
             language === 'ta' ? 'அருகிலுள்ள கிளையைக் கண்டுபிடி' :
             'Find Nearest Branch'}
          </h2>
          <p lang={language}>
            {language === 'hi' ? '"निकटतम शाखा खोजें" बोलकर अपने पास की IPPB शाखा ढूंढें।' :
             language === 'ta' ? '"அருகிலுள்ள கிளையைக் கண்டுபிடி" என்று சொல்லி உங்கள் அருகிலுள்ள IPPB கிளையைக் கண்டறியவும்.' :
             'Say "find nearest branch" to locate an IPPB branch near you.'}
          </p>
        </div>
      </section>

      <div className="cta-section">
        <Link to="/voice-banking" className="cta-button" aria-label={language === 'hi' ? 'वॉइस बैंकिंग शुरू करें' : 'தொடங்கு'}>
          {language === 'hi' ? 'वॉइस बैंकिंग शुरू करें →' :
           language === 'ta' ? 'குரல் வங்கியைத் தொடங்கு →' :
           'Start Voice Banking →'}
        </Link>
      </div>
    </div>
  );
}
