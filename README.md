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
git clone https://github.com/spinxog/Auto-Insurance-Project.git
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


Since the set time for coderbyte video was 1:30 minutes, I'll explain my desision here. I started by defining the requirements, data fields, and ensure privacy and compliance. I made sure say that everything is upfront but since this is only locally tested there is only a minimal privacy workflow for POC. For data collection,  I planned to use telemetry data, which includes speed, acceleration, braking, mileage and geolocation. There is a POC data generator since there isn't an avalible dataset but its thoughout carefully to imitate realistic data. However, problem with syntheic data is that its doesn't exactly capture real world sensor noise. The ETL was implemented to compute features in real-time, this was because it would allow the risk scoring model to use fresh data to make premiums dynamic. The problem with doing it this way is that its only s docker-based streaming that only for testing and demonstration which while it does maintain a scalable architecture, the acutal variables are unknown. For the risk scoring model, there are canonical features that are inputed, like max speed, harsh braking, rolling mileage, and night-time driving. Thses are implemented to be interpretable feature to ensure the model's explainability. The risk scoring itself I chose a Gradient boost model since its tree-based it would be more accurate for structured data, and it would be explainable via SHAP and deterministic when seeded. The problem with this approach is that a neural network/sequence based model could improve accuracy but we would need real data and also more telemetry data to test the full capability of the model. The pricing engine converts the rick score into premiums with guardlines to avoid extreme swings. I mkae it so it uses SHAP to explain which features influnced the premiums, but the probelm with this is that it simpilfied so the actuarial factions could be added. The react dashboard displays rick scores, trips, feature explanations and privacy controls. I chose to this way because it would be transparent, which would make users more engaged and allow for testing of privacy. Problem with this is there is any real-time devices streaming and it also need real GPS data. For scalable, security and infrastructure, I when with a docker compose setup which runs the full local stack with postgres, Redis, and streaming jobs. It makes sure that the entire pipeline is reproduceable and also scablable, however the limitation with this is that it doesn't include a full CI/CD pipeline and cloud deployment since the project scope was only tested locally. There were full integration tests ensureing reliability across ingestion, feature computation, risk scoring, and pricing with all tests passes but since there isnt a large scale stress test as it was only local its an unknown variable but the its fully functional and the correctness of entire pipeline is fully verified. 


---

Copyright (c) 2025 Pradip Debnath

All rights reserved.

This repository and its contents are provided solely for the purpose of evaluating the take-home assessment submission.

No other use, reproduction, distribution, modification, or commercial use is permitted without explicit written permission from the author.



