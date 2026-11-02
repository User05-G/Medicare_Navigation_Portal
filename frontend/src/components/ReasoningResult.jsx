import React from 'react';

export default function ReasoningResult({ reasoning }) {
  if (!reasoning) return null;

  if (!reasoning.success) {
    return (
      <div className="card" style={{ borderLeft: '4px solid var(--danger)', background: '#fef2f2' }}>
        <div style={{ color: '#991b1b', fontWeight: '700', marginBottom: '0.4rem' }}>
          ⚠️ Destination Not Identified
        </div>
        <p style={{ fontSize: '0.9rem', color: '#7f1d1d' }}>
          {reasoning.reason}
        </p>
      </div>
    );
  }

  return (
    <div className="reasoning-card">
      <div className="reasoning-header">
        🧠 Default Reasoning Engine (Rule-Based Matching)
      </div>

      <div className="reasoning-flow">
        <div className="reasoning-step">
          <span className="reasoning-badge">INPUT</span>
          <div>
            <strong>Requirement:</strong> "{reasoning.query}"
          </div>
        </div>

        <div className="reasoning-step">
          <span className="reasoning-badge" style={{ background: 'var(--accent-cyan)' }}>RULE MATCH</span>
          <div>
            Matched Keyword: <strong>"{reasoning.matched_keyword}"</strong>
          </div>
        </div>

        <div className="reasoning-step" style={{ background: '#dcfce7', borderColor: '#86efac' }}>
          <span className="reasoning-badge" style={{ background: 'var(--primary)' }}>DESTINATION</span>
          <div>
            Mapped Destination: <strong>{reasoning.destination_name}</strong> ({reasoning.destination_floor_name})
          </div>
        </div>
      </div>

      <div style={{ marginTop: '0.75rem', fontSize: '0.8rem', color: '#15803d', fontStyle: 'italic' }}>
        ℹ️ {reasoning.explanation}
      </div>
    </div>
  );
}
