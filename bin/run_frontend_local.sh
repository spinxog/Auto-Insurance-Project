#!/bin/bash
# Run frontend development server

set -e

echo "Starting frontend development server..."

# Set environment variables
export REACT_APP_API_BASE=http://localhost:8080

# Navigate to dashboard directory (assuming it exists)
cd src/dashboard

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    npm install
fi

# Start development server
npm run start
