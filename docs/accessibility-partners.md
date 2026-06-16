# Accessibility Partnership Contacts — OSAM Voice Banking

## NAB (National Association for the Blind)
- **Website:** https://www.nabindia.org
- **Contact:** NAB Delhi — Sector 5, Rohini, New Delhi — 110085
- **Phone:** +91-11-27052301 / 02
- **Email:** nab@nabindia.org.in
- **Reach out for:** Screen reader testing (NVDA/JAWS), blind user testing, feedback on voice prompts

## Ali Yavar Jung National Institute for the Deaf (AYJNIHH)
- **Website:** https://ayjnihh.nic.in
- **Contact:** AYJNIHH Mumbai — Bandra Reclamation, Mumbai — 400050
- **Phone:** +91-22-26400165
- **Email:** director@ayjnihh.nic.in
- **Reach out for:** Haptic feedback testing, voice prompt clarity for hard-of-hearing users, accessibility feedback

## Suggested Email Template

```
Subject: Partnership for Testing OSAM Voice Banking — Accessible Banking for Hindi & Tamil Users

Dear [Contact Person],

I am building OSAM, an open-source voice-enabled banking system integrated with 
India Post Payments Bank (IPPB). The system supports Hindi, Tamil, and English 
and is designed specifically for users who cannot read or see.

We have built:
- A 4-tab accessible web interface (Chat + Components + Loan + Compliance)
- IVR phone mode with Press 1/2/3 navigation in Hindi and Tamil
- Voice response audio via gTTS (Hindi) with plans for native Tamil recording
- Full WCAG 2.1 AA + IS 17802 compliance checking
- Screen reader support with proper ARIA roles, labels, and live regions

We would like to request your organization's help in testing OSAM with:
1. Blind users (screen reader testing with NVDA/TalkBack)
2. Deaf users (haptic feedback and visual indicator testing)
3. Elderly users (voice prompt clarity in Hindi and Tamil)

The prototype is live at: https://osam-voice-banking.onrender.com

We are happy to schedule a demo and incorporate your feedback.

Thank you,
[Your Name]
OSAM — Open Source Accessible Banking
```

## Testing Checklist (for NAB/AYJNIHH partners)

### Screen Reader (NVDA / TalkBack)
- [ ] All buttons have `aria-label` or visible text
- [ ] Tab order follows visual order
- [ ] Error messages are announced
- [ ] Step changes in loan form are announced
- [ ] Modal focus is trapped
- [ ] IVR keypad keys are announced as buttons

### Haptic Feedback
- [ ] Success: 1 short vibration (100ms)
- [ ] Error: 2 short vibrations (100ms + 150ms gap)
- [ ] Loading state: no vibration until complete
- [ ] Form submission: vibration on success/failure

### Voice Prompts (Hindi)
- [ ] Words are short and clear
- [ ] Numbers are spoken clearly
- [ ] Menu options are repeated on request
- [ ] No background noise interference with gTTS quality

### Voice Prompts (Tamil) — Requires native speaker
- [ ] Native speaker to review and record all Tamil prompts
- [ ] Replace gTTS Tamil audio with recorded files
- [ ] Test with elderly Tamil-speaking users
