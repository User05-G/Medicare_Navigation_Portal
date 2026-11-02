import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import NavigationForm from './components/NavigationForm';
import ReasoningResult from './components/ReasoningResult';
import NavigationResult from './components/NavigationResult';
import HospitalMap from './components/HospitalMap';
import AlgorithmComparison from './components/AlgorithmComparison';
import HowItWorks from './components/HowItWorks';
import About from './components/About';

import {
  fetchLocations,
  navigateDirect,
  navigateIntelligent
} from './services/api';

export default function App() {
  const [locations, setLocations] = useState([]);
  const [activeTab, setActiveTab] = useState('navigate');
  const [navResult, setNavResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState(null);

  // Initial location data loading from backend Flask API
  useEffect(() => {
    async function loadData() {
      try {
        const data = await fetchLocations();
        if (data.success && data.locations) {
          setLocations(data.locations);
        }
      } catch (err) {
        console.error('API Error:', err);
        setApiError('Unable to connect to Flask Backend Server (http://127.0.0.1:5000). Please verify backend is running.');
      }
    }
    loadData();
  }, []);

  const handleNavigate = async (params) => {
    setIsLoading(true);
    setApiError(null);
    try {
      let res;
      if (params.mode === 'direct') {
        res = await navigateDirect(params.start, params.destination, params.algorithm);
      } else {
        res = await navigateIntelligent(params.start, params.query, params.algorithm);
      }

      if (res) {
        setNavResult(res);
      }
    } catch (err) {
      console.error('Navigation error:', err);
      setApiError('Failed to calculate navigation route. Please check backend server status.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="main-content">
        {/* Hero Banner */}
        <div className="hero-banner">
          <h1 className="hero-title">Find Your Way Through MediCare</h1>
          <p className="hero-subtitle">
            Navigate departments, diagnostic services, and patient facilities across our three-floor hospital with intelligent destination identification and graph-based route planning.
          </p>
          <div className="hero-pills">
            <div className="hero-pill">
              🧠 Rule-Based Reasoning
            </div>
            <div className="hero-pill">
              ⚡ Custom BFS & A* Algorithms
            </div>
            <div className="hero-pill">
              🗺️ 2D Interactive Schematic Map
            </div>
            <div className="hero-pill">
              🏥 18 Locations • 3 Floors
            </div>
          </div>
        </div>

        {/* Backend API Error Banner */}
        {apiError && (
          <div className="card" style={{ borderLeft: '4px solid var(--danger)', background: '#fef2f2', color: '#991b1b', marginBottom: '1.5rem' }}>
            <strong>⚠️ Backend Connection Error:</strong> {apiError}
          </div>
        )}

        {/* Navigation Portal Tab */}
        {activeTab === 'navigate' && (
          <div className="nav-grid">
            <div>
              <NavigationForm
                locations={locations}
                onNavigate={handleNavigate}
                isLoading={isLoading}
              />

              {navResult && navResult.reasoning && (
                <ReasoningResult reasoning={navResult.reasoning} />
              )}
            </div>

            <div>
              {navResult && (
                <NavigationResult result={navResult} />
              )}

              <HospitalMap
                locations={locations}
                activeRoute={navResult?.route || []}
                activeStartId={navResult?.start?.id}
                activeDestId={navResult?.destination?.id}
              />
            </div>
          </div>
        )}

        {/* Algorithm Comparison Tab */}
        {activeTab === 'comparison' && (
          <AlgorithmComparison locations={locations} />
        )}

        {/* How It Works Tab */}
        {activeTab === 'howitworks' && (
          <HowItWorks />
        )}

        {/* About Tab */}
        {activeTab === 'about' && (
          <About />
        )}
      </main>

      <footer className="footer">
        <p>
          <strong>MediCare Hospital Patient Navigation System</strong> • Academic AI Mini-Project
        </p>
        <p style={{ marginTop: '0.25rem', fontSize: '0.75rem' }}>
          Rule-Based Default Reasoning + Graph-Search Algorithms (BFS & A*) • Simulated Hospital Graph
        </p>
      </footer>
    </div>
  );
}
