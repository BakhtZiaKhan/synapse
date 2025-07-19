'use client';

import { useState } from 'react';

function Spinner() {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', margin: '32px 0' }}>
      <div style={{
        width: 48,
        height: 48,
        border: '6px solid #d1d5db',
        borderTop: '6px solid #2563eb',
        borderRadius: '50%',
        animation: 'spin 1s linear infinite'
      }} />
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileInfo, setFileInfo] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [showSummary, setShowSummary] = useState(false);
  const [summaryData, setSummaryData] = useState<any>(null);
  const [transcript, setTranscript] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setFileInfo(
        `File: ${e.target.files[0].name} (${(e.target.files[0].size / 1024 / 1024).toFixed(2)} MB)`
      );
      setShowSummary(false);
      setSummaryData(null);
      setError(null);
    }
  }

  async function handleProcess() {
    setLoading(true);
    setShowSummary(false);
    setSummaryData(null);
    setError(null);
    setTranscript(null);
    try {
      // 1. Send audio to Whisper API
      const formData = new FormData();
      if (selectedFile) {
        formData.append('file', selectedFile);
      }
      const whisperRes = await fetch('http://localhost:7860/predict', {
        method: 'POST',
        body: formData,
      });
      if (!whisperRes.ok) throw new Error('Whisper API failed');
      const whisperData = await whisperRes.json();
      const transcriptText = whisperData.data && whisperData.data[0];
      if (!transcriptText) throw new Error('No transcript received');
      setTranscript(transcriptText);

      // 2. Send transcript to LLM API
      const llmRes = await fetch('http://localhost:7861/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          data: [transcriptText, 'json', 0.7, 512]
        }),
      });
      if (!llmRes.ok) throw new Error('LLM API failed');
      const llmData = await llmRes.json();
      let analysis = llmData.data && llmData.data[0];
      let parsed = null;
      try {
        parsed = JSON.parse(analysis);
      } catch {
        parsed = null;
      }
      if (!parsed) throw new Error('Could not parse LLM response');
      setSummaryData(parsed);
      setShowSummary(true);
    } catch (err: any) {
      setError(err.message || 'Processing failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="main-container">
      <h1>Synapse</h1>
      <p className="info" style={{ textAlign: 'center' }}>AI-Powered Meeting Assistant</p>
      <h2>Upload Your Meeting Recording</h2>
      <p>Get instant transcripts, summaries, and insights</p>
      <label htmlFor="file-upload">Choose File (.mp3 ,.wav, .m4a, .mp4, .mov,.mkv ) </label>
      <input
        id="file-upload"
        type="file"
        accept="audio/*,video/*"
        onChange={handleFileChange}
        disabled={loading}
      />
      {fileInfo && (
        <div className="success">{fileInfo}</div>
      )}
      <button
        disabled={!selectedFile || loading}
        onClick={handleProcess}
      >
        {loading ? 'Processing...' : selectedFile ? "Process Meeting" : "Select a file to continue"}
      </button>
      {loading && <Spinner />}
      {error && <div style={{ color: 'red', marginTop: 16 }}>{error}</div>}
      {showSummary && summaryData && (
        <div style={{ marginTop: 32, background: '#fff', borderRadius: 12, padding: 24, boxShadow: '0 2px 8px rgba(0,0,0,0.06)' }}>
          <h2 style={{ color: '#18181b', marginTop: 0 }}>Meeting Summary</h2>
          <h3 style={{ color: '#232326', marginBottom: 8 }}>Summary</h3>
          <p style={{ color: '#232326' }}>{summaryData.summary}</p>
          <h3 style={{ color: '#232326', marginBottom: 8 }}>Action Items</h3>
          <ul style={{ color: '#232326', paddingLeft: 20 }}>
            {summaryData.action_items && summaryData.action_items.map((item: string, idx: number) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
          <h3 style={{ color: '#232326', marginBottom: 8 }}>Key Decisions</h3>
          <ul style={{ color: '#232326', paddingLeft: 20 }}>
            {summaryData.key_decisions && summaryData.key_decisions.map((item: string, idx: number) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
          {transcript && (
            <div style={{ marginTop: 32 }}>
              <h3 style={{ color: '#232326', marginBottom: 8 }}>Transcript</h3>
              <pre style={{ background: '#f3f4f6', padding: 16, borderRadius: 8, color: '#232326', whiteSpace: 'pre-wrap', fontSize: 15 }}>{transcript}</pre>
            </div>
          )}
        </div>
      )}
      {!loading && !showSummary && <>
        <h2>AI Transcription</h2>
        <p>High-quality speech-to-text conversion powered by advanced AI models.</p>
        <h2>Smart Analysis</h2>
        <p>Extract key insights, action items, and decisions automatically.</p>
        <h2>Easy Upload</h2>
        <p>Support for all major audio and video formats. Drag and drop interface.</p>
        <footer>
          © 2025 Synapse Meeting Assistant.
        </footer>
      </>}
    </div>
  );
} 