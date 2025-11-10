import React from 'react';
import './TripList.css';

const TripList = ({ trips }) => {
  // Format date in a more human-friendly way
  const formatTripDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = now - date;
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return "Today";
    if (diffDays === 1) return "Yesterday";
    if (diffDays < 7) return `${diffDays} days ago`;
    return date.toLocaleDateString();
  };

  // Get a human-like description of the trip score
  const getTripScoreDescription = (score) => {
    if (score >= 80) return "Great driving!";
    if (score >= 70) return "Good trip";
    if (score >= 60) return "Okay";
    return "Needs improvement";
  };

  return (
    <div className="trip-list">
      <h2>Your Recent Drives</h2>
      {trips.length === 0 ? (
        <p>You haven't taken any trips yet. Start driving to see your data here!</p>
      ) : (
        <div className="trips-container">
          {trips.map((trip) => (
            <div key={trip.id} className="trip-card">
              <div className="trip-header">
                <span className="trip-date">
                  {formatTripDate(trip.start_time)}
                </span>
                <span className="trip-score">
                  {trip.score?.toFixed(1) || 'N/A'} - {getTripScoreDescription(trip.score)}
                </span>
              </div>
              <div className="trip-details">
                <div className="trip-metric">
                  <span className="metric-label">Miles driven:</span>
                  <span className="metric-value">{trip.distance_mi?.toFixed(1) || 'N/A'} miles</span>
                </div>
                <div className="trip-metric">
                  <span className="metric-label">Top speed:</span>
                  <span className="metric-value">{trip.max_speed?.toFixed(1) || 'N/A'} mph</span>
                </div>
                <div className="trip-metric">
                  <span className="metric-label">Sudden stops:</span>
                  <span className="metric-value">{trip.harsh_brakes || 0}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TripList;
