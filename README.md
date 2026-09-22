# OpsRelay | Cloud-Native Microservice & Kubernetes Deployment

OpsRelay is a lightweight microservice architecture designed to simulate automated container deployments, health monitoring, and self-healing incident response workflows.

---

## 📌 Features

### Phase 1 — Core Microservice
- **Containerized REST API:** Built with Python (FastAPI) and Uvicorn.
- **Health Check Endpoint:** Exposes `/health` returning real-time status and versioning.
- **Docker Integration:** Minimal `python:3.11-slim` base container environment.

### Phase 2 — Local Kubernetes Orchestration (Zero Cloud Cost)
- **Declarative Deployment:** Managed via Kubernetes manifests (`k8s/deployment.yaml`) with 2 load-balanced replicas.
- **Automated Health Probes:** Configured `livenessProbe` and `readinessProbe` checking `/health` every 5-10 seconds.
- **Service Networking:** Exposes pods to `localhost` using a Kubernetes `LoadBalancer` service.

---

## 🛠️ Prerequisites

- **Language:** Python 3.11+
- **Containerization:** Docker Desktop
- **Orchestration:** Kubernetes (`kubectl`) built into Docker Desktop
- **Tools:** Git, macOS Terminal

---

## 🚀 Getting Started

### 1. Build Local Image
bash
docker build -t opsrelay-app:latest ./app


### 2. Deploy to Kubernetes
bash
kubectl apply -f k8s/


### 3. Verify Deployment & Health Check
bash
kubectl get pods
curl http://localhost:8000/health


---

## 📁 Repository Structure

text
OpsRelay-AWS/
├── app/
│   ├── main.py          # FastAPI microservice
│   ├── Dockerfile       # Container definition
│   └── requirements.txt # Python dependencies
├── k8s/
│   ├── deployment.yaml  # Kubernetes Deployment & Probes
│   └── service.yaml     # Kubernetes Service (LoadBalancer)
├── .gitignore
└── README.md