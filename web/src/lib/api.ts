const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8002';

export async function processVoice(input: {
  text?: string;
  language?: string;
  session_id?: string;
}) {
  const res = await fetch(`${API_BASE}/api/voice/process`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...input, language: input.language || 'hi' }),
  });
  if (!res.ok) throw new Error('Voice processing failed');
  return res.json();
}

export async function checkBalance(accountNumber: string, language = 'hi') {
  const res = await fetch(`${API_BASE}/api/balance`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ account_number: accountNumber, language }),
  });
  if (!res.ok) throw new Error('Balance check failed');
  return res.json();
}

export async function applyLoan(amount: number, purpose: string, language = 'hi') {
  const res = await fetch(`${API_BASE}/api/loan/apply`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ amount, purpose, language }),
  });
  if (!res.ok) throw new Error('Loan application failed');
  return res.json();
}

export async function findBranch(location: string, language = 'hi') {
  const res = await fetch(`${API_BASE}/api/branch/nearby`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ location, language }),
  });
  if (!res.ok) throw new Error('Branch lookup failed');
  return res.json();
}

export async function getScripts(language: string) {
  const res = await fetch(`${API_BASE}/api/scripts/${language}`);
  if (!res.ok) throw new Error('Failed to load scripts');
  return res.json();
}

export async function uploadAudio(file: Blob, language = 'hi'): Promise<{ transcript: string; intent: string }> {
  const form = new FormData();
  form.append('file', file, 'recording.wav');
  form.append('language', language);
  const res = await fetch(`${API_BASE}/api/voice/upload`, {
    method: 'POST',
    body: form,
  });
  if (!res.ok) throw new Error('Audio upload failed');
  return res.json();
}

export function getAudioUrl(path: string): string {
  return `${API_BASE}${path}`;
}
