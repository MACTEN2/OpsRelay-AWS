# OpsRelay | Cloud-Native Microservice & Kubernetes Deployment

OpsRelay is a lightweight microservice architecture designed to simulate automated container deployments, health monitoring, self-healing incident response, and CI/CD pipelines.

---

## 📌 Architecture & Features

### Phase 1 — Core Microservice
- **Containerized REST API:** Built with Python (FastAPI) and Uvicorn.
- **Health Check Endpoint:** Exposes `/health` returning real-time status and versioning.
- **Docker Integration:** Minimal `python:3.11-slim` base container environment.

### Phase 2 — Local Kubernetes Orchestration (Zero Cloud Cost)
- **Declarative Deployment:** Managed via Kubernetes manifests (`k8s/deployment.yaml`) with 2 load-balanced replicas.
- **Automated Health Probes:** Configured `livenessProbe` and `readinessProbe` checking `/health` every 5-10 seconds.
- **Chaos Engineering:** `/chaos` fault-injection endpoint to verify Kubernetes self-healing and auto-restart capability.
- **Service Networking:** Exposes pods to `localhost` using a Kubernetes `LoadBalancer` service.

### Phase 3 — Automated CI/CD Pipeline (GitHub Actions)
- **Automated Testing:** Runs `pytest` and `flake8` linting on every push to `main`.
- **Automated Container Verification:** Verifies Docker builds automatically in GitHub Actions runners.

---

## 🛠️ Tech Stack & Prerequisites

- **Language:** Python 3.11+
- **Containerization:** Docker Desktop
- **Orchestration:** Kubernetes (`kubectl`) built into Docker Desktop
- **CI/CD:** GitHub Actions
- **Tools:** Git, macOS Terminal

---

## 🚀 Getting Started

### 1. Run Unit Tests Locally
```bash
PYTHONPATH=app pytest app/
2. Build Local Image & Deploy to Kubernetes
Bash
docker build -t opsrelay-app:latest ./app
kubectl apply -f k8s/
3. Test Chaos & Self-Healing
Bash
# Trigger fault
curl -X POST http://localhost:8000/chaos

# Watch Kubernetes automatically restart the broken container
kubectl get pods -w
📁 Repository Structure
Plaintext
OpsRelay-AWS/
├── .github/
│   └── workflows/
│       └── ci.yml       # GitHub Actions CI Pipeline
├── app/
│   ├── main.py          # FastAPI microservice
│   ├── test_main.py     # Pytest unit tests
│   ├── Dockerfile       # Container definition
│   └── requirements.txt # Python dependencies
├── k8s/
│   ├── deployment.yaml  # Kubernetes Deployment & Probes
│   └── service.yaml     # Kubernetes Service (LoadBalancer)
├── .gitignore
└── README.md

