import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import VoiceBankingPage from './pages/VoiceBankingPage';

export default function App() {
  return (
    <div className="app-container">
      <nav className="nav-bar" role="navigation" aria-label="मुख्य नेविगेशन">
        <Link to="/" className="nav-brand" aria-label="OSAM Voice Banking होम">
          🏦 OSAM
        </Link>
        <div className="nav-links">
          <Link to="/" className="nav-link" aria-current="page">
            होम
          </Link>
          <Link to="/voice-banking" className="nav-link">
            वॉइस बैंकिंग
          </Link>
        </div>
      </nav>
      <main className="main-content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/voice-banking" element={<VoiceBankingPage />} />
        </Routes>
      </main>
      <footer className="app-footer" role="contentinfo">
        <p>OSAM Voice Banking — RBI Innovation Hub प्रोजेक्ट</p>
        <p lang="ta">OSAM குரல் வங்கி — RBI புதுமை மையத் திட்டம்</p>
      </footer>
    </div>
  );
}
