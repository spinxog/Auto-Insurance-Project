import React, { useState } from 'react';
import { updateConsent, requestDataExport, requestDataDeletion } from '../services/api';
import './PrivacySettings.css';

const PrivacySettings = () => {
  const [consent, setConsent] = useState({
    telematics: true,
    location: 'exact',
    data_retention: true
  });
  const [exportStatus, setExportStatus] = useState(null);
  const [deleteStatus, setDeleteStatus] = useState(null);

  const handleConsentChange = async (field, value) => {
    const newConsent = { ...consent, [field]: value };
    setConsent(newConsent);

    try {
      await updateConsent('user123', newConsent);
      alert('Consent updated successfully');
    } catch (error) {
      alert('Failed to update consent');
    }
  };

  const handleDataExport = async () => {
    try {
      const result = await requestDataExport('user123');
      setExportStatus(result);
    } catch (error) {
      alert('Failed to request data export');
    }
  };

  const handleDataDeletion = async () => {
    if (window.confirm('Are you sure you want to delete all your data? This action cannot be undone.')) {
      try {
        const result = await requestDataDeletion('user123');
        setDeleteStatus(result);
      } catch (error) {
        alert('Failed to request data deletion');
      }
    }
  };

  return (
    <div className="privacy-settings">
      <h2>Your Privacy Controls</h2>

      <div className="settings-section">
        <h3>What We Collect</h3>
        <div className="consent-options">
          <label className="consent-option">
            <input
              type="checkbox"
              checked={consent.telematics}
              onChange={(e) => handleConsentChange('telematics', e.target.checked)}
            />
            Share my driving data to get personalized insurance rates
          </label>

          <div className="location-precision">
            <label>How precise should location tracking be?</label>
            <select
              value={consent.location}
              onChange={(e) => handleConsentChange('location', e.target.value)}
              disabled={!consent.telematics}
            >
              <option value="exact">Precise (best for accurate pricing)</option>
              <option value="coarse">General area (city level)</option>
              <option value="aggregated">Broad region (more privacy)</option>
            </select>
          </div>

          <label className="consent-option">
            <input
              type="checkbox"
              checked={consent.data_retention}
              onChange={(e) => handleConsentChange('data_retention', e.target.checked)}
            />
            Keep my data for up to 3 years (helps with claims and better rates)
          </label>
        </div>
      </div>

      <div className="settings-section">
        <h3>Your Data Rights</h3>
        <div className="data-actions">
          <button onClick={handleDataExport} className="action-button export">
            Download My Data
          </button>
          <button onClick={handleDataDeletion} className="action-button delete">
            Delete Everything
          </button>
        </div>

        {exportStatus && (
          <div className="status-message success">
            <strong>Download Request:</strong> {exportStatus.message}
            {exportStatus.request_id && <span> (Request #{exportStatus.request_id})</span>}
          </div>
        )}

        {deleteStatus && (
          <div className="status-message warning">
            <strong>Deletion Request:</strong> {deleteStatus.message}
            {deleteStatus.request_id && <span> (Request #{deleteStatus.request_id})</span>}
          </div>
        )}
      </div>

      <div className="settings-section">
        <h3>How We Use Your Data</h3>
        <div className="info-text">
          <p>We use your driving information to:</p>
          <ul>
            <li>Give you insurance rates that match your driving style</li>
            <li>Show you tips to drive more safely</li>
            <li>Make claims easier when you need them</li>
            <li>Help improve safety for everyone (your personal data stays private)</li>
          </ul>
          <p>Your information is always protected with strong security. You can change your mind anytime.</p>
        </div>
      </div>
    </div>
  );
};

export default PrivacySettings;
