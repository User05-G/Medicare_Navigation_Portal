import React from 'react';

export default function Navbar({ activeTab, setActiveTab }) {
  return (
    <header className="navbar">
      <div className="navbar-inner">
        <a href="#home" className="brand" onClick={() => setActiveTab('navigate')}>
          <div className="brand-icon">+</div>
          <div>
            <div className="brand-title">MediCare</div>
            <div className="brand-subtitle">Hospital Patient Navigation System</div>
          </div>
        </a>

        <nav className="nav-tabs">
          <button
            className={`nav-btn ${activeTab === 'navigate' ? 'active' : ''}`}
            onClick={() => setActiveTab('navigate')}
          >
            🧭 Navigation Portal
          </button>
          <button
            className={`nav-btn ${activeTab === 'comparison' ? 'active' : ''}`}
            onClick={() => setActiveTab('comparison')}
          >
            ⚖️ Algorithm Comparison
          </button>
          <button
            className={`nav-btn ${activeTab === 'howitworks' ? 'active' : ''}`}
            onClick={() => setActiveTab('howitworks')}
          >
            💡 How It Works
          </button>
          <button
            className={`nav-btn ${activeTab === 'about' ? 'active' : ''}`}
            onClick={() => setActiveTab('about')}
          >
            ℹ️ About Project
          </button>
        </nav>
      </div>
    </header>
  );
}
