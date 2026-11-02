import React, { useState } from 'react';
import { compareAlgorithms } from '../services/api';

export default function AlgorithmComparison({ locations }) {
  const [startId, setStartId] = useState('F2'); // Default: Neurology
  const [destId, setDestId] = useState('S1'); // Default: Patient Wards
  const [comparison, setComparison] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleCompare = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const res = await compareAlgorithms(startId, destId);
      setComparison(res);
    } catch (err) {
      console.error('Comparison error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="card">
      <h2 className="card-title">⚖️ Algorithm Comparison: BFS vs A* Search</h2>
      <p style={{ color: 'var(--text-muted)', marginBottom: '1.25rem', fontSize: '0.95rem' }}>
        Compare Breadth-First Search (Connection-Based) and A* Search (Distance-Aware Heuristic) side-by-side on the weighted hospital graph.
      </p>

      <form onSubmit={handleCompare} style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginBottom: '1.5rem', alignItems: 'flex-end' }}>
        <div style={{ flex: 1, minWidth: '200px' }}>
          <label className="form-label">Start Location</label>
          <select className="form-select" value={startId} onChange={(e) => setStartId(e.target.value)}>
            {locations.map(l => (
              <option key={l.id} value={l.id}>
                {l.name} ({l.floor_name})
              </option>
            ))}
          </select>
        </div>

        <div style={{ flex: 1, minWidth: '200px' }}>
          <label className="form-label">Destination Location</label>
          <select className="form-select" value={destId} onChange={(e) => setDestId(e.target.value)}>
            {locations.map(l => (
              <option key={l.id} value={l.id}>
                {l.name} ({l.floor_name})
              </option>
            ))}
          </select>
        </div>

        <button type="submit" className="btn-primary" style={{ width: 'auto' }} disabled={isLoading}>
          {isLoading ? 'Comparing...' : ' Run Comparison'}
        </button>
      </form>

      {comparison && (
        <div>
          <table className="comp-table">
            <thead>
              <tr>
                <th>Feature Metric</th>
                <th>BFS (Breadth-First Search)</th>
                <th>A* (A-Star Search)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Search Principle</strong></td>
                <td>Level-by-level queue traversal ignoring edge weights during search.</td>
                <td>Evaluates $f(n) = g(n) + h(n)$ with priority min-heap queue.</td>
              </tr>
              <tr>
                <td><strong>Optimization Goal</strong></td>
                <td>Minimizes number of edge connections (hops).</td>
                <td>Minimizes actual physical walking distance in metres.</td>
              </tr>
              <tr>
                <td><strong>Route Discovered</strong></td>
                <td><code>{comparison.bfs.route?.join(' → ')}</code></td>
                <td><code>{comparison.astar.route?.join(' → ')}</code></td>
              </tr>
              <tr>
                <td><strong>Physical Distance</strong></td>
                <td><strong>{comparison.bfs.distance} metres</strong></td>
                <td><strong>{comparison.astar.distance} metres</strong></td>
              </tr>
              <tr>
                <td><strong>Connection Steps</strong></td>
                <td>{comparison.bfs.edge_count} steps</td>
                <td>{comparison.astar.edge_count} steps</td>
              </tr>
              <tr>
                <td><strong>Walking Time</strong></td>
                <td>{comparison.bfs.estimated_time}</td>
                <td>{comparison.astar.estimated_time}</td>
              </tr>
              <tr>
                <td><strong>Execution Time</strong></td>
                <td>{comparison.bfs.execution_time_ms} ms</td>
                <td>{comparison.astar.execution_time_ms} ms</td>
              </tr>
            </tbody>
          </table>

          <div style={{ marginTop: '1.25rem', padding: '1rem', background: 'var(--bg-card-subtle)', borderRadius: 'var(--radius-md)', fontSize: '0.9rem' }}>
            💡 <strong>Key Takeaway:</strong> BFS treats all graph connections as 1 step (unweighted) to find the minimum number of transitions. A* utilizes physical edge weights + floor transition heuristic $h(n)$ to discover the shortest walking path.
          </div>
        </div>
      )}
    </div>
  );
}
