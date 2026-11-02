import React from 'react';

export default function About() {
  return (
    <div className="card">
      <h2 className="card-title">ℹ️ About MediCare Patient Navigation System</h2>
      <p style={{ fontSize: '1rem', color: 'var(--text-muted)', marginBottom: '1.25rem', lineHeight: '1.6' }}>
        The <strong>MediCare Hospital Patient Navigation System</strong> is an academic AI mini-project demonstrating how <strong>rule-based Default Reasoning</strong> and <strong>graph-search algorithms (BFS & A*)</strong> collaborate to solve indoor hospital navigation.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
        <div style={{ background: 'var(--bg-card-subtle)', padding: '1rem', borderRadius: 'var(--radius-md)' }}>
          <h3 style={{ fontSize: '0.95rem', marginBottom: '0.4rem', color: 'var(--primary)' }}>
            🤖 AI Concepts Demonstrated
          </h3>
          <ul style={{ paddingLeft: '1.2rem', fontSize: '0.85rem', color: 'var(--text-dark)', lineHeight: '1.6' }}>
            <li>Rule-Based Default Reasoning engine for natural prompt interpretation.</li>
            <li>Unweighted Breadth-First Search (BFS) for connection-based pathing.</li>
            <li>A* Search ($f(n) = g(n) + h(n)$) with admissible floor-transition heuristic.</li>
            <li>Dynamic path distance and walking time calculation.</li>
          </ul>
        </div>

        <div style={{ background: 'var(--bg-card-subtle)', padding: '1rem', borderRadius: 'var(--radius-md)' }}>
          <h3 style={{ fontSize: '0.95rem', marginBottom: '0.4rem', color: 'var(--primary)' }}>
            🏥 Hospital Structure
          </h3>
          <ul style={{ paddingLeft: '1.2rem', fontSize: '0.85rem', color: 'var(--text-dark)', lineHeight: '1.6' }}>
            <li>3 Floors: Ground Floor, First Floor, Second Floor.</li>
            <li>18 Defined Hospital Locations.</li>
            <li>17 Bidirectional Weighted Graph Connections.</li>
            <li>Dedicated Vertical Stair/Elevator Connector Nodes (G7, F6, S5).</li>
          </ul>
        </div>
      </div>

      <div style={{ background: '#fffbe6', border: '1px solid #ffe58f', padding: '1rem', borderRadius: 'var(--radius-md)' }}>
        <h4 style={{ color: '#873800', marginBottom: '0.4rem', fontSize: '0.9rem' }}>
          ⚠️ Project Scope & Academic Disclaimers:
        </h4>
        <ul style={{ paddingLeft: '1.2rem', fontSize: '0.8rem', color: '#612500', lineHeight: '1.5' }}>
          <li>The hospital layout, location node IDs, and edge distances are simulated for academic demonstration.</li>
          <li>Default Reasoning performs keyword matching to identify hospital service departments and does NOT provide medical diagnosis.</li>
          <li>No external machine learning frameworks, databases, or third-party AI APIs are used.</li>
          <li>All search algorithms (BFS and A*) are custom implemented in Python without external graph libraries.</li>
        </ul>
      </div>
    </div>
  );
}
