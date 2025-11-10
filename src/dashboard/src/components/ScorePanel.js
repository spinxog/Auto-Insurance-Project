// ScorePanel component for displaying risk score and explanation

import React from 'react';
import './ScorePanel.css';

const ScorePanel = ({ riskScore, modelVersion, topFeatures }) => {
  // Function to convert feature names to human-readable format
  const getHumanReadableFeature = (featureName) => {
    const featureMap = {
      'f_trip_max_speed': 'Max Speed',
      'f_trip_avg_accel': 'Average Acceleration',
      'f_trip_harsh_brake_count': 'Harsh Braking Events',
      'f_trip_night_driving_minutes': 'Night Driving Time',
      'f_policy_monthly_miles_30d': 'Monthly Miles Driven',
      'f_policy_percent_city_driving': 'City Driving Percentage',
      'f_policy_percent_highway': 'Highway Driving Percentage'
    };
    return featureMap[featureName] || featureName;
  };

  // Function to format contribution values
  const formatContribution = (contribution) => {
    if (contribution > 0) {
      return `+${contribution.toFixed(2)}`;
    }
    return contribution.toFixed(2);
  };

  // Generate human-like explanation based on score
  const getScoreDescription = (score) => {
    if (score >= 80) return "Excellent driving! You're a very safe driver.";
    if (score >= 70) return "Good job! Your driving habits are quite safe.";
    if (score >= 60) return "Not bad, but there's room for improvement.";
    if (score >= 50) return "Your driving could be safer. Let's work on that.";
    return "Safety first! Consider improving your driving habits.";
  };

  return (
    <div className="score-panel">
      <h2>Your Driving Score</h2>
      <div className="score-display">
        <span className="score-value">{riskScore.toFixed(1)}</span>
        <span className="score-label">out of 100</span>
      </div>
      <p className="score-description">{getScoreDescription(riskScore)}</p>
      <div className="explanation">
        <h3>What affects your score:</h3>
        <ul>
          {topFeatures.map((feature, index) => (
            <li key={index}>
              {getHumanReadableFeature(feature.feature)}: {formatContribution(feature.contribution)}
            </li>
          ))}
        </ul>
        <p className="explanation-note">
          Higher scores mean safer driving and potentially lower insurance costs.
        </p>
      </div>
    </div>
  );
};

export default ScorePanel;
