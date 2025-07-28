import React, { useState } from 'react';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [summary, setSummary] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [timeStats, setTimeStats] = useState(null);

  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [translatedSummary, setTranslatedSummary] = useState('');

  const handleSummarize = async () => {
    setLoading(true);
    setError('');
    setSummary('');
    setTimeStats(null);
    setTranslatedSummary('');

    try {
      const response = await fetch('http://localhost:5000/summarize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });
      const data = await response.json();
      if (data.summary) {
        setSummary(data.summary);
        setTimeStats(data.time_taken);
      } else {
        setError(data.error || 'Failed to summarize');
      }
    } catch (err) {
      setError('Server error');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    try {
      const response = await fetch('http://localhost:5000/summarize/pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) throw new Error('PDF download failed');

      const blob = await response.blob();
      const urlBlob = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = urlBlob;
      a.download = 'summary.pdf';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    } catch (err) {
      setError('Failed to download PDF');
    }
  };

  const handleTranslate = async () => {
    try {
      const response = await fetch('http://localhost:5000/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: summary, target_lang: selectedLanguage }),
      });

      const data = await response.json();
      if (data.translated_text) {
        setTranslatedSummary(data.translated_text);
      } else {
        setError('Translation failed');
      }
    } catch (err) {
      setError('Translation error');
    }
  };

  return (
    <div className="main-container">
      <div className="left-panel">
        <h2>📰 Quick Blog Summarizer</h2>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter blog/article URL"
        />
        <div className="button-group">
          <button onClick={handleSummarize} disabled={loading || !url}>Summarize</button>
          <button onClick={handleDownloadPDF} disabled={!summary}>Download PDF</button>
        </div>
        {error && <p className="error">⚠️ {error}</p>}
      </div>

      <div className="right-panel">
        <h3>📄 Summary</h3>
        {loading ? <p>⏳ Summarizing...</p> : <p>{summary}</p>}

        {timeStats && (
          <div className="time-stats">
            <h4>⏱️ Time Taken:</h4>
            <p>📥 Download: <strong>{timeStats.download_time_sec}s</strong></p>
            <p>🧠 Summarization: <strong>{timeStats.summary_time_sec}s</strong></p>
            <p>🕒 Total: <strong>{timeStats.total_time_sec}s</strong></p>
          </div>
        )}

        {summary && (
          <div className="translation-section">
            <h4>🌐 Translate Summary</h4>
            <select value={selectedLanguage} onChange={(e) => setSelectedLanguage(e.target.value)}>
              <option value="en">English</option>
              <option value="hi">Hindi</option>
              <option value="te">Telugu</option>
            </select>
            <button onClick={handleTranslate}>Translate</button>

            {translatedSummary && (
              <div className="translated-summary">
                <h4>🌍 Translated Summary:</h4>
                <p>{translatedSummary}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
