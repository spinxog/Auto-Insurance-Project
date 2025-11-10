# Auto Insurance Telematics Pipeline

A local streaming telematics pipeline for auto insurance risk assessment with explainability and privacy-by-design.

---

## Architecture

```
Device/SDK → Secure Ingestion → Streaming ETL → Feature Store → Risk-Scoring ML Models → Pricing Engine → User Dashboard
```

---

## Quick Start (Local)

### Prerequisites

* Docker & Docker Compose
* Python 3.8+
* Node.js 16+ (for dashboard)

### Setup

```bash
git clone <repo>
cd auto-insurance-project
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run Locally

```bash
# Start local stack
./bin/run_local_stack.sh

# Generate sample telemetry data
./bin/generate_poc_data.sh

# Train baseline ML model
./bin/train_local.sh

# Run tests
./bin/run_tests.sh

# Start React dashboard
./bin/run_frontend_local.sh
```

Open the dashboard at: [http://localhost:3000](http://localhost:3000)

---

## Project Structure

```
src/        # Core source code (ingestion, features, models, serving, dashboard)
models/     # Trained model artifacts
data/       # Sample telemetry and features
docs/       # Documentation & diagrams
bin/        # Executable scripts
tests/      # Unit & integration tests
infra/      # Local Docker setup
```

---

## Key Features

* **Risk Scoring**: GBM model with deterministic training
* **Pricing Engine**: Converts risk score → premium
* **Explainability**: Top feature contributions (SHAP)
* **Privacy**: Data export & deletion endpoints for testing
* **Dashboard**: View risk scores, trips, and model explanations

---

## API Endpoints (Sample)

* `GET /users/{id}/driving-scores` → Risk scores
* `GET /users/{id}/trips/{trip_id}` → Trip details
* `POST /users/{id}/consent` → Manage consent
* `GET /pricing/explanation/{policy_id}` → Premium explanation

---

Copyright (c) 2025 Pradip Debnath

All rights reserved.

This repository and its contents are provided solely for the purpose of evaluating [Your Name]’s take-home assessment submission.

No other use, reproduction, distribution, modification, or commercial use is permitted without explicit written permission from the author.



