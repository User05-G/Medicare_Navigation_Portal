import React, { useState } from 'react';

export default function NavigationForm({ locations, onNavigate, isLoading }) {
  const [mode, setMode] = useState('direct'); // 'direct' or 'intelligent'
  const [startId, setStartId] = useState('G1'); // Default: Main Entrance
  const [destinationId, setDestinationId] = useState('S1'); // Default: Patient Wards
  const [query, setQuery] = useState('');
  const [algorithm, setAlgorithm] = useState('astar'); // 'astar' or 'bfs'

  const samplePrompts = [
    "I need a blood test",
    "I have a broken leg",
    "I need medicine",
    "chest pain",
    "I have an ear problem",
    "emergency",
    "I need physical therapy"
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (mode === 'direct') {
      onNavigate({
        mode: 'direct',
        start: startId,
        destination: destinationId,
        algorithm
      });
    } else {
      if (!query.trim()) return;
      onNavigate({
        mode: 'intelligent',
        start: startId,
        query: query.trim(),
        algorithm
      });
    }
  };

  const groundLocs = locations.filter(l => l.floor === 0);
  const firstLocs = locations.filter(l => l.floor === 1);
  const secondLocs = locations.filter(l => l.floor === 2);

  return (
    <div className="card">
      <h2 className="card-title">📍 Navigation Control Panel</h2>

      {/* Mode Switcher */}
      <div className="mode-toggle">
        <button
          type="button"
          className={`mode-btn ${mode === 'direct' ? 'active' : ''}`}
          onClick={() => setMode('direct')}
        >
          🎯 Direct Navigation
        </button>
        <button
          type="button"
          className={`mode-btn ${mode === 'intelligent' ? 'active' : ''}`}
          onClick={() => setMode('intelligent')}
        >
          🧠 Intelligent Navigation
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        {/* Start Location */}
        <div className="form-group">
          <label className="form-label">Current Location (Start Point)</label>
          <select
            className="form-select"
            value={startId}
            onChange={(e) => setStartId(e.target.value)}
          >
            <optgroup label="Ground Floor">
              {groundLocs.map(l => (
                <option key={l.id} value={l.id}>
                  {l.name} ({l.id})
                </option>
              ))}
            </optgroup>
            <optgroup label="First Floor">
              {firstLocs.map(l => (
                <option key={l.id} value={l.id}>
                  {l.name} ({l.id})
                </option>
              ))}
            </optgroup>
            <optgroup label="Second Floor">
              {secondLocs.map(l => (
                <option key={l.id} value={l.id}>
                  {l.name} ({l.id})
                </option>
              ))}
            </optgroup>
          </select>
        </div>

        {/* Direct Mode: Destination Select */}
        {mode === 'direct' ? (
          <div className="form-group">
            <label className="form-label">Destination</label>
            <select
              className="form-select"
              value={destinationId}
              onChange={(e) => setDestinationId(e.target.value)}
            >
              <optgroup label="Ground Floor">
                {groundLocs.map(l => (
                  <option key={l.id} value={l.id}>
                    {l.name} ({l.id})
                  </option>
                ))}
              </optgroup>
              <optgroup label="First Floor">
                {firstLocs.map(l => (
                  <option key={l.id} value={l.id}>
                    {l.name} ({l.id})
                  </option>
                ))}
              </optgroup>
              <optgroup label="Second Floor">
                {secondLocs.map(l => (
                  <option key={l.id} value={l.id}>
                    {l.name} ({l.id})
                  </option>
                ))}
              </optgroup>
            </select>
          </div>
        ) : (
          /* Intelligent Mode: Text Requirement Input */
          <div className="form-group">
            <label className="form-label">What do you need?</label>
            <input
              type="text"
              className="form-input"
              placeholder="e.g. 'I need a blood test' or 'broken bone'"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <div className="chip-list">
              {samplePrompts.map((prompt, idx) => (
                <button
                  type="button"
                  key={idx}
                  className="chip"
                  onClick={() => setQuery(prompt)}
                >
                  "{prompt}"
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Algorithm Selection */}
        <div className="form-group">
          <label className="form-label">Search Algorithm</label>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
            <label style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              padding: '0.6rem',
              border: `1px solid ${algorithm === 'astar' ? 'var(--primary)' : 'var(--border)'}`,
              borderRadius: 'var(--radius-md)',
              background: algorithm === 'astar' ? 'var(--primary-glow)' : 'white',
              cursor: 'pointer',
              fontSize: '0.85rem',
              fontWeight: '600'
            }}>
              <input
                type="radio"
                name="algorithm"
                value="astar"
                checked={algorithm === 'astar'}
                onChange={() => setAlgorithm('astar')}
              />
              A* (Distance-Aware)
            </label>

            <label style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              padding: '0.6rem',
              border: `1px solid ${algorithm === 'bfs' ? 'var(--primary)' : 'var(--border)'}`,
              borderRadius: 'var(--radius-md)',
              background: algorithm === 'bfs' ? 'var(--primary-glow)' : 'white',
              cursor: 'pointer',
              fontSize: '0.85rem',
              fontWeight: '600'
            }}>
              <input
                type="radio"
                name="algorithm"
                value="bfs"
                checked={algorithm === 'bfs'}
                onChange={() => setAlgorithm('bfs')}
              />
              BFS (Connection-Based)
            </label>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          className="btn-primary"
          disabled={isLoading || (mode === 'intelligent' && !query.trim())}
        >
          {isLoading ? 'Calculating Route...' : mode === 'direct' ? '🚀 Find Optimal Route' : '🧠 Identify Destination & Route'}
        </button>
      </form>
    </div>
  );
}
