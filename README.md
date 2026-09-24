# Fraud Detection Platform

A lightweight end-to-end fraud detection project that combines a machine learning pipeline, FastAPI backend, Streamlit interface, MySQL persistence, and AWS deployment setup.

## Overview

This project is designed to demonstrate the full workflow of a fraud detection system:

- data preparation and feature engineering
- model training and threshold optimization
- REST API serving and authentication
- web dashboard for interaction
- Dockerized local deployment
- Terraform-based AWS infrastructure

## Features

- Machine learning pipeline with LightGBM and temporal train/validation/test splits
- Feature engineering for transaction and identity data
- Validation-based decision threshold optimization
- FastAPI backend with JWT authentication
- MySQL-backed user and prediction history storage
- Streamlit frontend for model interaction
- Docker-based local setup
- MLflow experiment tracking
- Terraform deployment setup for AWS

## Architecture

```mermaid
graph TD
    User[User] -->|HTTP| Streamlit[Streamlit App]
    Streamlit -->|API requests| FastAPI[FastAPI API]
    FastAPI -->|Inference| Model[LightGBM Model]
    FastAPI -->|Reads/Writes| DB[(MySQL)]
```

The main components are:

- Streamlit app for user interaction
- FastAPI backend for authentication and prediction endpoints
- LightGBM model for inference
- MySQL database for storing users and prediction records
- Terraform for AWS infrastructure provisioning

## Tech Stack

- Python
- Pandas, NumPy, scikit-learn, LightGBM
- FastAPI, Pydantic, SQLAlchemy
- MySQL, Alembic
- Streamlit
- MLflow
- Docker, Docker Compose
- pytest, Ruff
- Terraform

## Quick Start

### Prerequisites

- Python 3.13+
- Docker and Docker Compose
- Git

### 1) Clone the repository

```bash
git clone <repository-url>
cd fraud_detection
```

### 2) Configure environment variables

Create a `.env` file in the project root and set the required values. Example:

```env
MODEL_PATH=models/fraud_detection_model.joblib
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3308/fraud_detection
TEST_DATABASE_URL=mysql+pymysql://root:your_password@localhost:3308/test_fraud_detection
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=your_password
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRES_MINUTES=15
REFRESH_TOKEN_EXPIRES_DAYS=7
MYSQL_DATABASE=fraud_detection
MYSQL_USER=fraud_api
MYSQL_PASSWORD=your_mysql_password
MYSQL_ROOT_PASSWORD=your_root_password
API_URL=http://fastapi:8000
```

> Adjust the database values to match your local or Docker setup. The app expects a valid database connection at startup.

### 3) Run with Docker Compose

```bash
docker compose up --build
```

This starts:

- MySQL database
- Alembic migrations
- FastAPI API
- Streamlit app

Available endpoints:

| Service | URL |
| --- | --- |
| API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |
| Streamlit | http://localhost:8501 |

To stop the services:

```bash
docker compose down
```

To remove the database volume too:

```bash
docker compose down -v
```

## Local Development

If you want to run the backend and frontend outside Docker:

```bash
uvicorn src.api.main:app --reload
streamlit run streamlit_app/app.py
```

## Database Migrations

The database schema is managed with Alembic:

```bash
alembic upgrade head
```

## Model

The project uses a LightGBM classifier trained on the IEEE-CIS fraud dataset. The workflow includes:

1. data loading and merging
2. feature engineering
3. validation-based threshold optimization
4. model evaluation
5. final model artifact creation

The trained model is stored in the `models/` directory and is loaded by the FastAPI application at startup.

## Validation Highlights

| Metric | Validation |
| --- | --- |
| PR-AUC | ~0.412 |
| ROC-AUC | ~0.893 |
| Precision | ~0.451 |
| Recall | ~0.425 |
| F1-score | ~0.438 |

The optimized threshold for the final classifier was around `0.18`.

## Testing and Quality Checks

Run the test suite:

```bash
pytest
```

Run linting:

```bash
ruff check .
```

## Project Structure

```text
fraud_detection/
├── alembic/                 # Database migrations
├── models/                  # Trained model artifacts
├── notebooks/               # ML exploration and training notebooks
├── scripts/                 # Utility scripts
├── src/                     # Backend source code
├── streamlit_app/           # Streamlit frontend
├── terraform/               # AWS infrastructure files
├── .env                     # Local environment variables
├── Dockerfile               # FastAPI container
├── Dockerfile.streamlit     # Streamlit container
├── docker-compose.yml       # Local service orchestration
├── pyproject.toml           # Project config and tooling
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── alembic.ini              # Alembic config
```

## Notes

- MLflow is used for experiment tracking and model development.
- The API does not require a live MLflow server at inference time.
- This project is built around a real-world fraud detection problem and uses a temporal split to better reflect production conditions.

## Deployment

The repository includes Terraform configuration for AWS infrastructure, including application and foundation layers for ECS, ALB, ECR, and RDS resources.

The application infrastructure can be destroyed independently from the long-lived resources when needed:

```bash
cd terraform/application
terraform destroy
```

And recreated later with:

```bash
cd terraform/application
terraform apply
```

