import React, { useRef, useState, useCallback, useEffect } from 'react';

interface VoiceRecorderProps {
  onTranscript: (text: string) => void;
  language: string;
  disabled?: boolean;
}

declare global {
  interface Window {
    SpeechRecognition: any;
    webkitSpeechRecognition: any;
  }
}

export default function VoiceRecorder({ onTranscript, language, disabled }: VoiceRecorderProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [browserSupport, setBrowserSupport] = useState<'webkit' | 'standard' | 'none'>('none');
  const recognitionRef = useRef<any>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  useEffect(() => {
    if (window.SpeechRecognition) setBrowserSupport('standard');
    else if (window.webkitSpeechRecognition) setBrowserSupport('webkit');
    else setBrowserSupport('none');
  }, []);

  const langMap: Record<string, string> = {
    hi: 'hi-IN',
    ta: 'ta-IN',
    en: 'en-IN',
  };

  const startWebSpeech = useCallback(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return;

    const recognition = new SpeechRecognition();
    recognition.lang = langMap[language] || 'hi-IN';
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      onTranscript(transcript);
    };

    recognition.onerror = () => {
      setIsRecording(false);
    };

    recognition.onend = () => {
      setIsRecording(false);
    };

    recognitionRef.current = recognition;
    recognition.start();
    setIsRecording(true);
  }, [language, onTranscript]);

  const startMediaRecorder = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        chunksRef.current = [];
        stream.getTracks().forEach((t) => t.stop());
        onTranscript(`audio_recording:${blob.size}bytes`);
      };

      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start();
      setIsRecording(true);

      setTimeout(() => {
        if (mediaRecorder.state === 'recording') {
          mediaRecorder.stop();
          setIsRecording(false);
        }
      }, 5000);
    } catch {
      setIsRecording(false);
    }
  }, [onTranscript]);

  const toggleRecording = useCallback(() => {
    if (isRecording) {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
        mediaRecorderRef.current.stop();
      }
      setIsRecording(false);
      return;
    }

    if (browserSupport !== 'none') {
      startWebSpeech();
    } else {
      startMediaRecorder();
    }
  }, [isRecording, browserSupport, startWebSpeech, startMediaRecorder]);

  return (
    <div className="voice-recorder" role="region" aria-label="वॉइस इनपुट">
      <button
        onClick={toggleRecording}
        disabled={disabled}
        className={`record-btn ${isRecording ? 'recording' : ''}`}
        aria-label={isRecording ? 'रिकॉर्डिंग बंद करें' : 'वॉइस कमांड के लिए रिकॉर्ड करें'}
        aria-pressed={isRecording}
      >
        <span className="mic-icon" aria-hidden="true">
          {isRecording ? '🔴' : '🎤'}
        </span>
        <span className="record-label">
          {isRecording ? 'सुन रहा है...' : 'बोलें'}
        </span>
      </button>
      {browserSupport === 'none' && (
        <p className="a11y-hint" role="status">
          आपका ब्राउज़र वॉइस रिकॉग्निशन सपॉर्ट नहीं करता। कृपया टेक्स्ट टाइप करें या Chrome उपयोग करें।
        </p>
      )}
    </div>
  );
}
