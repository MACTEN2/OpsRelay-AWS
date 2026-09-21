# OpsRelay-AWS | Automated Cloud Deployment & Fault Recovery Engine

OpsRelay-AWS is a lightweight, cloud-native microservice architecture designed to simulate real-world developer and SRE incident response workflows, automated container deployments, and health monitoring.

## 📌 Features (Phase 1 - Core Microservice)

- **Containerized REST API:** Built with Python (FastAPI) and Uvicorn.
- **Health Check Endpoint:** Exposes a standard `/health` endpoint returning real-time application status and versioning.
- **Docker Integration:** Isolated container environment utilizing a minimal `python:3.11-slim` base image.

## 🛠️ Tech Stack & Prerequisites

- **Language:** Python 3.11+
- **Framework:** FastAPI / Uvicorn
- **Containerization:** Docker Desktop
- **Tools:** Git, macOS Terminal

## 🚀 Running Locally

### 1. Build the Docker Image
```bash
docker build -t opsrelay-app ./app