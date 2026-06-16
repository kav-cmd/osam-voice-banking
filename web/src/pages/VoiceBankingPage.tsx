import React, { useState, useRef, useEffect } from 'react';
import VoiceRecorder from '../components/VoiceRecorder';
import AccessibleButton from '../components/AccessibleButton';
import { processVoice, checkBalance, applyLoan, findBranch, getAudioUrl } from '../lib/api';

type Step = 'idle' | 'menu' | 'balance_account' | 'balance_result' | 'loan_purpose' | 'loan_amount' | 'loan_confirm' | 'loan_result' | 'branch_location' | 'branch_result';

export default function VoiceBankingPage() {
  const [language, setLanguage] = useState('hi');
  const [step, setStep] = useState<Step>('idle');
  const [sessionId, setSessionId] = useState<string>('');
  const [transcript, setTranscript] = useState('');
  const [responseText, setResponseText] = useState('');
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [history, setHistory] = useState<{ role: 'user' | 'system'; text: string }[]>([]);
  const chatRef = useRef<HTMLDivElement>(null);

  const loanDataRef = useRef({ purpose: '', amount: 0 });

  const langLabels = {
    hi: { title: 'वॉइस बैंकिंग', badge: 'वॉइस बैंकिंग', inputPlaceholder: 'यहाँ टेक्स्ट टाइप करें या बोलें...', send: 'भेजें' },
    ta: { title: 'குரல் வங்கி', badge: 'குரல் வங்கி', inputPlaceholder: 'இங்கே தட்டச்சு செய்க அல்லது பேசுங்கள்...', send: 'அனுப்பு' },
    en: { title: 'Voice Banking', badge: 'VOICE BANKING', inputPlaceholder: 'Type here or speak...', send: 'Send' },
  }[language];

  useEffect(() => {
    chatRef.current?.scrollTo({ top: chatRef.current.scrollHeight, behavior: 'smooth' });
  }, [history]);

  const handleTextInput = async (text: string) => {
    if (!text.trim() || loading) return;
    setTranscript(text);
    setHistory((h) => [...h, { role: 'user', text }]);
    setLoading(true);
    setError('');

    try {
      const res = await processVoice({ text, language, session_id: sessionId || undefined });
      setSessionId(res.session_id);
      setResponseText(res.response_text);
      setAudioUrl(res.audio_url || null);
      setHistory((h) => [...h, { role: 'system', text: res.response_text }]);
      setStep(mapIntentToStep(res.intent));
    } catch (e: any) {
      setError(e.message || 'कृपया पुनः प्रयास करें');
    } finally {
      setLoading(false);
    }
  };

  const handleTranscript = async (text: string) => {
    if (text.startsWith('audio_recording:')) {
      setLoading(true);
      try {
        const res = await processVoice({ text: 'voice command received', language, session_id: sessionId || undefined });
        setSessionId(res.session_id);
        setResponseText(res.response_text);
        setAudioUrl(res.audio_url || null);
        setHistory((h) => [...h, { role: 'user', text: '🎤 [वॉइस इनपुट]' }, { role: 'system', text: res.response_text }]);
        setStep(mapIntentToStep(res.intent));
      } catch (e: any) {
        setError(e.message || 'वॉइस प्रोसेसिंग विफल');
      } finally {
        setLoading(false);
      }
    } else {
      await handleTextInput(text);
    }
  };

  const mapIntentToStep = (intent: string): Step => {
    switch (intent) {
      case 'balance': return 'balance_account';
      case 'loan': return 'loan_purpose';
      case 'branch': return 'branch_location';
      case 'goodbye': return 'idle';
      default: return 'menu';
    }
  };

  const handleBalanceSubmit = async (account: string) => {
    setLoading(true);
    try {
      const res = await checkBalance(account, language);
      setResponseText(res.response_text);
      setAudioUrl(res.audio_url || null);
      setHistory((h) => [...h, { role: 'user', text: `खाता: ${account}` }, { role: 'system', text: res.response_text }]);
      setStep('balance_result');
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleLoanPurpose = async (purpose: string) => {
    loanDataRef.current.purpose = purpose;
    setHistory((h) => [...h, { role: 'user', text: purpose }]);

    const promptText = {
      hi: `कृपया लोन राशि बताएं।`,
      ta: `கடன் தொகையைக் கூறுங்கள்।`,
      en: `Please state the loan amount.`,
    }[language];
    setResponseText(promptText);
    setHistory((h) => [...h, { role: 'system', text: promptText }]);
    setStep('loan_amount');
  };

  const handleLoanAmount = async (amountStr: string) => {
    const amount = parseFloat(amountStr.replace(/[^0-9.]/g, ''));
    if (isNaN(amount) || amount <= 0) {
      setError({
        hi: 'कृपया सही राशि दर्ज करें',
        ta: 'சரியான தொகையை உள்ளிடவும்',
        en: 'Please enter a valid amount',
      }[language]);
      return;
    }
    loanDataRef.current.amount = amount;
    setHistory((h) => [...h, { role: 'user', text: `₹${amount}` }]);

    const confirmText = {
      hi: `क्या आप ₹${amount} का लोन ${loanDataRef.current.purpose} के लिए आवेदन करना चाहते हैं? हां के लिए 1, रद्द के लिए 2 दबाएं।`,
      ta: `நீங்கள் ₹${amount} கடனை ${loanDataRef.current.purpose}க்காக விண்ணப்பிக்க விரும்புகிறீர்களா? ஆம் எனில் 1, ரத்து செய்ய 2 அழுத்தவும்.`,
      en: `Do you want to apply for a loan of ₹${amount} for ${loanDataRef.current.purpose}? Press 1 for yes, 2 to cancel.`,
    }[language];
    setResponseText(confirmText);
    setHistory((h) => [...h, { role: 'system', text: confirmText }]);
    setStep('loan_confirm');
  };

  const handleLoanConfirm = async (confirm: boolean) => {
    if (!confirm) {
      const cancelText = { hi: 'लोन आवेदन रद्द कर दिया गया।', ta: 'கடன் விண்ணப்பம் ரத்து செய்யப்பட்டது.', en: 'Loan application cancelled.' }[language];
      setResponseText(cancelText);
      setHistory((h) => [...h, { role: 'user', text: 'नहीं' }, { role: 'system', text: cancelText }]);
      setStep('idle');
      return;
    }
    setLoading(true);
    try {
      const res = await applyLoan(loanDataRef.current.amount, loanDataRef.current.purpose, language);
      setResponseText(res.response_text);
      setAudioUrl(res.audio_url || null);
      setHistory((h) => [...h, { role: 'user', text: 'हाँ' }, { role: 'system', text: res.response_text }]);
      setStep('loan_result');
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleBranchSubmit = async (location: string) => {
    setLoading(true);
    try {
      const res = await findBranch(location, language);
      setResponseText(res.response_text);
      setAudioUrl(res.audio_url || null);
      setHistory((h) => [...h, { role: 'user', text: location }, { role: 'system', text: res.response_text }]);
      setStep('branch_result');
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const resetSession = () => {
    setStep('idle');
    setSessionId('');
    setTranscript('');
    setResponseText('');
    setAudioUrl(null);
    setHistory([]);
    setError('');
  };

  const [customInput, setCustomInput] = useState('');

  return (
    <div className="page voice-page">
      <div className="voice-header">
        <div>
          <span className="badge">{langLabels.badge}</span>
          <h1>{langLabels.title}</h1>
        </div>
        <div className="lang-selector-sm" role="radiogroup" aria-label="भाषा">
          {['hi', 'ta', 'en'].map((l) => (
            <button
              key={l}
              onClick={() => setLanguage(l)}
              className={`lang-sm ${language === l ? 'active' : ''}`}
              role="radio"
              aria-checked={language === l}
            >
              {{ hi: 'हि', ta: 'த', en: 'En' }[l]}
            </button>
          ))}
        </div>
      </div>

      <div className="chat-container" ref={chatRef} role="log" aria-label="चैट हिस्ट्री" aria-live="polite">
        {history.length === 0 && (
          <div className="welcome-msg">
            <p lang={language}>
              {language === 'hi' ? 'नमस्कार! मैं OSAM हूँ। आप कह सकते हैं: "मेरा बैलेंस चेक करें", "लोन के लिए आवेदन करें", या "निकटतम शाखा खोजें"।' :
               language === 'ta' ? 'வணக்கம்! நான் OSAM. நீங்கள் சொல்லலாம்: "என் இருப்பைச் சரிபார்", "கடனுக்கு விண்ணப்பி", அல்லது "அருகிலுள்ள கிளையைக் கண்டுபிடி".' :
               'Hello! I am OSAM. You can say: "check my balance", "apply for a loan", or "find nearest branch".'}
            </p>
          </div>
        )}

        {history.map((msg, i) => (
          <div key={i} className={`chat-msg ${msg.role}`} lang={language}>
            <div className="msg-bubble">{msg.text}</div>
          </div>
        ))}

        {loading && (
          <div className="chat-msg system">
            <div className="msg-bubble loading-dots">
              <span>.</span><span>.</span><span>.</span>
            </div>
          </div>
        )}

        {error && (
          <div className="chat-msg system" role="alert">
            <div className="msg-bubble error-msg">⚠️ {error}</div>
          </div>
        )}
      </div>

      <div className="voice-controls">
        <VoiceRecorder onTranscript={handleTranscript} language={language} disabled={loading} />

        <div className="text-input-row">
          <input
            type="text"
            value={customInput}
            onChange={(e) => setCustomInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && customInput.trim()) {
                handleTextInput(customInput.trim());
                setCustomInput('');
              }
            }}
            placeholder={langLabels.inputPlaceholder}
            className="text-input"
            aria-label={langLabels.inputPlaceholder}
            lang={language}
            disabled={loading}
          />
          <AccessibleButton
            onClick={() => {
              if (customInput.trim()) {
                handleTextInput(customInput.trim());
                setCustomInput('');
              }
            }}
            label={langLabels.send}
            description={langLabels.send}
            disabled={loading || !customInput.trim()}
          />
        </div>

        <div className="action-chips" role="group" aria-label="त्वरित क्रियाएँ">
          <button className="chip" onClick={() => handleTextInput('मेरा बैलेंस चेक करें')} lang={language}>
            💰 {language === 'hi' ? 'बैलेंस' : language === 'ta' ? 'இருப்பு' : 'Balance'}
          </button>
          <button className="chip" onClick={() => handleTextInput('लोन के लिए आवेदन करें')} lang={language}>
            📋 {language === 'hi' ? 'लोन' : language === 'ta' ? 'கடன்' : 'Loan'}
          </button>
          <button className="chip" onClick={() => handleTextInput('निकटतम शाखा खोजें')} lang={language}>
            📍 {language === 'hi' ? 'शाखा' : language === 'ta' ? 'கிளை' : 'Branch'}
          </button>
          <button className="chip" onClick={resetSession}>
            🔄 {language === 'hi' ? 'रीसेट' : language === 'ta' ? 'மீட்டமை' : 'Reset'}
          </button>
        </div>
      </div>
    </div>
  );
}
