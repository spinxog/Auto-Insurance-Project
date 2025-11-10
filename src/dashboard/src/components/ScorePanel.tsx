// ScorePanel component for displaying risk score and explanation

import React from 'react';

interface TopFeature {
  feature: string;
  contribution: number;
}

interface ScorePanelProps {
  riskScore: number;
  modelVersion: string;
  topFeatures: TopFeature[];
}

const ScorePanel: React.FC<ScorePanelProps> = ({ riskScore, modelVersion, topFeatures }) => {
  return (
    <div className="score-panel">
      <h2>Driving Risk Score</h2>
      <div className="score-display">
        <span className="score-value">{riskScore.toFixed(1)}</span>
        <span className="score-label">/100</span>
      </div>
      <div className="model-info">
        Model: {modelVersion}
      </div>
      <div className="explanation">
        <h3>Top reasons for this score:</h3>
        <ul>
          {topFeatures.map((feature, index) => (
            <li key={index}>
              {feature.feature}: {feature.contribution > 0 ? '+' : ''}{feature.contribution.toFixed(2)}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ScorePanel;
