import React, { useState, useEffect } from 'react';
import './App.css';
import ScorePanel from './components/ScorePanel';
import TripList from './components/TripList';
import PrivacySettings from './components/PrivacySettings';
import { getDrivingScores, getTrips } from './services/api';

function App() {
  const [scores, setScores] = useState(null);
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [scoresData, tripsData] = await Promise.all([
        getDrivingScores('user123'),
        getTrips('user123')
      ]);
      setScores(scoresData);
      setTrips(tripsData);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="loading-spinner"></div>
        <p>Loading your driving data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error">
        <h2>Oops! Something went wrong</h2>
        <p>We couldn't load your dashboard right now. Please try again later.</p>
        <button onClick={loadDashboardData} className="retry-button">Try Again</button>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Your Driving Dashboard</h1>
        <p>Track your safe driving habits and see how they affect your insurance</p>
      </header>
      <main className="App-main">
        <div className="dashboard-grid">
          <div className="score-section">
            {scores && <ScorePanel
              riskScore={scores.current_score}
              modelVersion={scores.model_version}
              topFeatures={scores.top_features || []}
            />}
          </div>
          <div className="trips-section">
            <TripList trips={trips} />
          </div>
          <div className="privacy-section">
            <PrivacySettings />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
