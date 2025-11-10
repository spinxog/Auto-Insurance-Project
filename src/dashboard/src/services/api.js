import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE || 'http://localhost:8080';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Mock data for development when backend is not available
const mockScores = {
  current_score: 65.4,
  model_version: 'v20251109_1',
  top_features: [
    { feature: 'f_trip_max_speed', contribution: 0.45 },
    { feature: 'f_trip_avg_accel', contribution: 0.32 },
    { feature: 'f_trip_harsh_brake_count', contribution: 0.18 }
  ]
};

const mockTrips = [
  {
    id: 'trip-001',
    start_time: '2025-11-09T08:30:00Z',
    end_time: '2025-11-09T09:15:00Z',
    distance_mi: 15.7,
    max_speed: 52.9,
    harsh_brakes: 2,
    score: 68.5
  },
  {
    id: 'trip-002',
    start_time: '2025-11-09T17:45:00Z',
    end_time: '2025-11-09T18:30:00Z',
    distance_mi: 11.6,
    max_speed: 44.8,
    harsh_brakes: 0,
    score: 62.3
  }
];

export const getDrivingScores = async (userId) => {
  try {
    const response = await api.get(`/users/${userId}/driving-scores`);
    return response.data;
  } catch (error) {
    console.warn('Backend not available, using mock data');
    return mockScores;
  }
};

export const getTrips = async (userId) => {
  try {
    const response = await api.get(`/users/${userId}/trips`);
    return response.data.trips || [];
  } catch (error) {
    console.warn('Backend not available, using mock data');
    return mockTrips;
  }
};

export const getTripDetails = async (userId, tripId) => {
  try {
    const response = await api.get(`/users/${userId}/trips/${tripId}`);
    return response.data;
  } catch (error) {
    console.warn('Backend not available, using mock data');
    return mockTrips.find(trip => trip.id === tripId) || null;
  }
};

export const getPricingExplanation = async (policyId) => {
  try {
    const response = await api.get(`/pricing/explanation/${policyId}`);
    return response.data;
  } catch (error) {
    console.warn('Backend not available, using mock data');
    return {
      risk_score: 65.4,
      top_features: mockScores.top_features,
      model_version: mockScores.model_version,
      explanation: 'Your driving score is based on speed, acceleration patterns, and braking behavior.'
    };
  }
};

export const updateConsent = async (userId, consentData) => {
  try {
    const response = await api.post(`/users/${userId}/consent`, consentData);
    return response.data;
  } catch (error) {
    console.warn('Backend not available, consent update simulated');
    return { status: 'success', message: 'Consent updated' };
  }
};

export const requestDataExport = async (userId) => {
  try {
    const response = await api.post(`/users/${userId}/export`);
    return response.data;
  } catch (error) {
    console.warn('Backend not available, export request simulated');
    return { status: 'pending', request_id: 'req-123', message: 'Export request submitted' };
  }
};

export const requestDataDeletion = async (userId) => {
  try {
    const response = await api.post(`/users/${userId}/delete`);
    return response.data;
  } catch (error) {
    console.warn('Backend not available, deletion request simulated');
    return { status: 'pending', request_id: 'del-456', message: 'Deletion request submitted' };
  }
};
