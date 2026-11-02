import React from 'react';

export default function HowItWorks() {
  return (
    <div className="card">
      <h2 className="card-title">💡 How MediCare Navigation Works</h2>
      <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem', fontSize: '1rem' }}>
        The system separates <strong>Destination Identification</strong> from <strong>Path Planning</strong>:
      </p>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        gap: '1.25rem',
        marginBottom: '2rem'
      }}>
        <div style={{ background: '#f0fdf4', border: '1px solid #bbf7d0', padding: '1.25rem', borderRadius: 'var(--radius-md)' }}>
          <div style={{ color: '#15803d', fontWeight: '800', fontSize: '1.1rem', marginBottom: '0.5rem' }}>
            01 — UNDERSTAND & REASON
          </div>
          <div style={{ fontWeight: '700', fontSize: '0.95rem', marginBottom: '0.4rem', color: '#166534' }}>
            Default Reasoning System
          </div>
          <p style={{ fontSize: '0.85rem', color: '#166534', lineHeight: '1.5' }}>
            When a user inputs a natural requirement like <em>"I need a blood test"</em>, the rule-based Default Reasoning engine matches keywords against predefined mapping rules to identify the target department: <strong>Laboratory (G5)</strong>.
          </p>
        </div>

        <div style={{ background: '#eff6ff', border: '1px solid #bfdbfe', padding: '1.25rem', borderRadius: 'var(--radius-md)' }}>
          <div style={{ color: '#1d4ed8', fontWeight: '800', fontSize: '1.1rem', marginBottom: '0.5rem' }}>
            02 — GRAPH SEARCH
          </div>
          <div style={{ fontWeight: '700', fontSize: '0.95rem', marginBottom: '0.4rem', color: '#1e40af' }}>
            BFS / A* Path Optimization
          </div>
          <p style={{ fontSize: '0.85rem', color: '#1e40af', lineHeight: '1.5' }}>
            Once the destination is confirmed, the custom Graph Search algorithms (unweighted BFS or distance-aware A* with floor-transition heuristic) search the 18-location weighted hospital adjacency graph to calculate the path.
          </p>
        </div>

        <div style={{ background: '#f5f3ff', border: '1px solid #ddd6fe', padding: '1.25rem', borderRadius: 'var(--radius-md)' }}>
          <div style={{ color: '#6d28d9', fontWeight: '800', fontSize: '1.1rem', marginBottom: '0.5rem' }}>
            03 — VISUAL NAVIGATE
          </div>
          <div style={{ fontWeight: '700', fontSize: '0.95rem', marginBottom: '0.4rem', color: '#5b21b6' }}>
            Interactive 2D SVG Map
          </div>
          <p style={{ fontSize: '0.85rem', color: '#5b21b6', lineHeight: '1.5' }}>
            The calculated route, total physical distance in metres, estimated walking time, and step-by-step directions are rendered visually on the 3-floor schematic SVG indoor hospital map.
          </p>
        </div>
      </div>

      <div style={{ background: 'var(--bg-card-subtle)', padding: '1.25rem', borderRadius: 'var(--radius-md)' }}>
        <h3 style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>Core Architectural Principle:</h3>
        <pre style={{
          background: '#0f172a',
          color: '#38bdf8',
          padding: '1rem',
          borderRadius: 'var(--radius-sm)',
          fontSize: '0.85rem',
          overflowX: 'auto',
          lineHeight: '1.6'
        }}>
{`                 MEDICARE
                    │
          ┌─────────┴─────────┐
          │                   │
  DEFAULT REASONING       GRAPH SEARCH
          │                   │
  "Where should I go?"   "How do I get there?"
          │                   │
          ↓                   ↓
   Destination          BFS / A*
          └─────────┬─────────┘
                    ↓
              NAVIGATION`}
        </pre>
      </div>
    </div>
  );
}
