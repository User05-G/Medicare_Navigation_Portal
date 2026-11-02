import React from 'react';

export default function NavigationResult({ result }) {
  if (!result || !result.success) return null;

  const {
    start,
    destination,
    algorithm,
    search_type,
    distance,
    estimated_time,
    edge_count,
    route_steps,
    execution_time_ms
  } = result;

  return (
    <div className="card">
      <h2 className="card-title">🗺️ Navigation Route Summary</h2>

      {/* Summary Metrics */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-label">Start Location</div>
          <div className="metric-value" style={{ fontSize: '1.1rem' }}>{start.name}</div>
          <div className="metric-sub">{start.floor_name}</div>
        </div>

        <div className="metric-card" style={{ borderColor: 'var(--primary-light)' }}>
          <div className="metric-label">Destination</div>
          <div className="metric-value" style={{ fontSize: '1.1rem', color: 'var(--primary-dark)' }}>
            {destination.name}
          </div>
          <div className="metric-sub">{destination.floor_name}</div>
        </div>

        <div className="metric-card">
          <div className="metric-label">Route Distance</div>
          <div className="metric-value">{distance} m</div>
          <div className="metric-sub">{edge_count} connection steps</div>
        </div>

        <div className="metric-card">
          <div className="metric-label">Walking Time</div>
          <div className="metric-value">{estimated_time}</div>
          <div className="metric-sub">@ 1.2 m/s avg speed</div>
        </div>

        <div className="metric-card">
          <div className="metric-label">Algorithm</div>
          <div className="metric-value" style={{ fontSize: '1.1rem' }}>{algorithm}</div>
          <div className="metric-sub">{execution_time_ms} ms computation</div>
        </div>
      </div>

      <div style={{
        background: 'var(--bg-card-subtle)',
        padding: '0.65rem 1rem',
        borderRadius: 'var(--radius-md)',
        fontSize: '0.85rem',
        color: 'var(--text-muted)',
        marginBottom: '1rem'
      }}>
        ℹ️ <strong>Search Strategy:</strong> {search_type}
      </div>

      {/* Route Timeline Steps */}
      <h3 style={{ fontSize: '1rem', marginBottom: '0.75rem' }}>
        🚩 Step-by-Step Path Directions:
      </h3>

      <div className="timeline">
        {route_steps.map((step, idx) => (
          <div
            key={idx}
            className={`timeline-item ${step.is_connector ? 'connector' : ''}`}
          >
            <div className="timeline-index">
              {step.step_index}
            </div>

            <div className="timeline-details">
              <div className="timeline-name">
                {step.name}
                {idx === 0 && <span style={{ marginLeft: '0.5rem', color: 'var(--success)', fontSize: '0.8rem' }}>(Current)</span>}
                {idx === route_steps.length - 1 && <span style={{ marginLeft: '0.5rem', color: 'var(--danger)', fontSize: '0.8rem' }}>(Destination)</span>}
              </div>
              <div className="timeline-floor">
                {step.floor_name} • Type: {step.type}
              </div>
            </div>

            {step.is_connector && (
              <span style={{
                background: 'var(--warning)',
                color: 'white',
                fontSize: '0.75rem',
                fontWeight: '700',
                padding: '0.2rem 0.5rem',
                borderRadius: '4px'
              }}>
                🛗 Stair / Elevator
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
