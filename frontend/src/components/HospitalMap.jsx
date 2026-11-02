import React, { useState, useEffect } from 'react';

export default function HospitalMap({ locations, activeRoute, activeStartId, activeDestId }) {
  const [activeFloor, setActiveFloor] = useState(0);

  // Auto-switch active floor when activeRoute changes to destination floor or start floor
  useEffect(() => {
    if (activeStartId) {
      const startLoc = locations.find(l => l.id === activeStartId);
      if (startLoc) {
        setActiveFloor(startLoc.floor);
      }
    }
  }, [activeStartId, activeRoute, locations]);

  // Edges on each floor for schematic corridor line rendering
  const floorEdges = {
    0: [
      { u: 'G1', v: 'G2' },
      { u: 'G2', v: 'G3' },
      { u: 'G2', v: 'G4' },
      { u: 'G2', v: 'G5' },
      { u: 'G2', v: 'G6' },
      { u: 'G2', v: 'G7' }
    ],
    1: [
      { u: 'F6', v: 'F1' },
      { u: 'F6', v: 'F2' },
      { u: 'F6', v: 'F3' },
      { u: 'F6', v: 'F4' },
      { u: 'F6', v: 'F5' }
    ],
    2: [
      { u: 'S5', v: 'S1' },
      { u: 'S5', v: 'S2' },
      { u: 'S5', v: 'S3' },
      { u: 'S5', v: 'S4' }
    ]
  };

  const currentFloorLocations = locations.filter(l => l.floor === activeFloor);

  // Extract route sub-path segments that belong to the active floor
  const getActiveFloorRouteSegments = () => {
    if (!activeRoute || activeRoute.length < 2) return [];
    
    const segments = [];
    for (let i = 0; i < activeRoute.length - 1; i++) {
      const uId = activeRoute[i];
      const vId = activeRoute[i + 1];
      
      const uLoc = locations.find(l => l.id === uId);
      const vLoc = locations.find(l => l.id === vId);

      // Same-floor segment
      if (uLoc && vLoc && uLoc.floor === activeFloor && vLoc.floor === activeFloor) {
        segments.push({ u: uLoc, v: vLoc });
      }
    }
    return segments;
  };

  const routeSegmentsOnFloor = getActiveFloorRouteSegments();

  return (
    <div className="map-container">
      <div className="map-header">
        <h2 style={{ fontSize: '1.25rem' }}>🗺️ 2D Interactive Floor Plan</h2>

        {/* Floor Switcher Tabs */}
        <div className="floor-tabs">
          <button
            className={`floor-tab ${activeFloor === 0 ? 'active' : ''}`}
            onClick={() => setActiveFloor(0)}
          >
            Ground Floor
          </button>
          <button
            className={`floor-tab ${activeFloor === 1 ? 'active' : ''}`}
            onClick={() => setActiveFloor(1)}
          >
            1st Floor
          </button>
          <button
            className={`floor-tab ${activeFloor === 2 ? 'active' : ''}`}
            onClick={() => setActiveFloor(2)}
          >
            2nd Floor
          </button>
        </div>
      </div>

      {/* SVG Viewport */}
      <div className="svg-viewport">
        <svg viewBox="0 0 500 580" className="map-svg">
          {/* Subtle Grid Pattern Background */}
          <defs>
            <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
              <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#1e293b" strokeWidth="0.5" />
            </pattern>
            <filter id="glow">
              <feGaussianBlur stdDeviation="4" result="coloredBlur" />
              <feMerge>
                <feMergeNode in="coloredBlur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          <rect width="100%" height="100%" fill="#0f172a" />
          <rect width="100%" height="100%" fill="url(#grid)" opacity="0.6" />

          {/* Render Schematic Corridor Lines */}
          {floorEdges[activeFloor]?.map((edge, idx) => {
            const uLoc = currentFloorLocations.find(l => l.id === edge.u);
            const vLoc = currentFloorLocations.find(l => l.id === edge.v);
            if (!uLoc || !vLoc) return null;
            return (
              <line
                key={`edge-${idx}`}
                x1={uLoc.x}
                y1={uLoc.y}
                x2={vLoc.x}
                y2={vLoc.y}
                className="corridor-line"
              />
            );
          })}

          {/* Render Highlighted Route Segments on Active Floor */}
          {routeSegmentsOnFloor.map((seg, idx) => (
            <line
              key={`route-seg-${idx}`}
              x1={seg.u.x}
              y1={seg.u.y}
              x2={seg.v.x}
              y2={seg.v.y}
              className="route-polyline"
            />
          ))}

          {/* Render Rooms / Nodes */}
          {currentFloorLocations.map((loc) => {
            const isStart = loc.id === activeStartId;
            const isDest = loc.id === activeDestId;
            const isInRoute = activeRoute && activeRoute.includes(loc.id);

            let nodeFill = "#1e293b";
            let nodeStroke = "#475569";
            let textFill = "#cbd5e1";

            if (isStart) {
              nodeFill = "#064e3b";
              nodeStroke = "#10b981";
              textFill = "#a7f3d0";
            } else if (isDest) {
              nodeFill = "#7f1d1d";
              nodeStroke = "#ef4444";
              textFill = "#fecaca";
            } else if (isInRoute) {
              nodeFill = "#0f766e";
              nodeStroke = "#06b6d4";
              textFill = "#ffffff";
            }

            const boxWidth = loc.type === "Connector" ? 120 : 110;
            const boxHeight = 44;

            return (
              <g key={loc.id} className="room-node" transform={`translate(${loc.x - boxWidth/2}, ${loc.y - boxHeight/2})`}>
                <rect
                  width={boxWidth}
                  height={boxHeight}
                  rx="8"
                  fill={nodeFill}
                  stroke={nodeStroke}
                  strokeWidth={isStart || isDest || isInRoute ? "2.5" : "1.5"}
                />

                {/* Node Label */}
                <text
                  x={boxWidth / 2}
                  y={18}
                  textAnchor="middle"
                  fill={textFill}
                  fontSize="11"
                  fontWeight="700"
                >
                  {loc.name}
                </text>

                <text
                  x={boxWidth / 2}
                  y={32}
                  textAnchor="middle"
                  fill="#94a3b8"
                  fontSize="9.5"
                  fontWeight="500"
                >
                  [{loc.id}] • {loc.type}
                </text>

                {/* Pulse animations for Start and Destination */}
                {isStart && (
                  <circle
                    cx={boxWidth / 2}
                    cy={boxHeight / 2}
                    r="24"
                    fill="none"
                    stroke="#10b981"
                    strokeWidth="2"
                    className="route-pulse"
                  />
                )}

                {isDest && (
                  <circle
                    cx={boxWidth / 2}
                    cy={boxHeight / 2}
                    r="24"
                    fill="none"
                    stroke="#ef4444"
                    strokeWidth="2"
                    className="route-pulse"
                  />
                )}
              </g>
            );
          })}
        </svg>
      </div>

      {/* Map Legend */}
      <div className="map-legend">
        <div className="legend-item">
          <div className="legend-dot start"></div>
          <span>🟢 Current / Start Location</span>
        </div>
        <div className="legend-item">
          <div className="legend-dot dest"></div>
          <span>🔴 Destination</span>
        </div>
        <div className="legend-item">
          <div className="legend-line"></div>
          <span>Cyan Line = Calculated Route</span>
        </div>
        <div className="legend-item">
          <div className="legend-icon"></div>
          <span>Stairs/Elevator = Floor Connector</span>
        </div>
      </div>
    </div>
  );
}
