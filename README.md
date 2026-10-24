# 🚀 DevOps Pipeline Lab

An end-to-end DevOps project: a containerized API deployed to Kubernetes on AWS — infrastructure as code, Helm charts, and Prometheus/Grafana observability built in.

![Python](https://img.shields.io/badge/Python-FastAPI-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?logo=terraform&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-EKS-FF9900?logo=amazonaws&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?logo=grafana&logoColor=white)

> Personal portfolio project — built to demonstrate a production-style DevOps workflow from code to running cluster.

## What it demonstrates

- **Containers** — Docker build, non-root runtime user, health checks
- **Infrastructure as Code** — Terraform provisions the AWS VPC, subnets, and EKS cluster
- **Kubernetes** — plain manifests plus a Helm chart for repeatable deploys
- **Observability** — Prometheus scraping + a Grafana dashboard for the app and nodes

## Deployment flow

```
Build Docker image
   │
   ▼
Push image to GHCR
   │
   ▼
kubectl apply -f k8s/   (or: helm upgrade --install devops-lab helm/devops-lab)
   │
   ▼
Kubernetes (EKS)
   ├─▶ app Deployment (2 replicas) + Service
   └─▶ Prometheus scrapes /metrics → Grafana dashboards
```

## Architecture

```
┌──────────────┐     ┌───────────────────────┐     ┌──────────────┐
│ GitHub repo  │────▶│ Docker image → GHCR   │────▶│  AWS EKS     │
│              │     │ kubectl / Helm deploy │     │  cluster     │
└──────────────┘     └───────────────────────┘     └──────┬───────┘
                                                          │
                                    ┌──────────────┐        ▼
                                    │  Prometheus  │  app Pods (FastAPI)
                                    │  + Grafana   │  Service (LoadBalancer)
                                    └──────────────┘
```

## Run it locally

```bash
# API only
cd app && pip install -r requirements.txt && uvicorn main:app --reload

# Full stack (app + Prometheus + Grafana)
docker compose up --build
# App: http://localhost:8000  ·  Prometheus: http://localhost:9090  ·  Grafana: http://localhost:3000
```

## Deploy to AWS (Terraform + Kubernetes)

```bash
cd terraform
terraform init
terraform apply          # provisions VPC, subnets, EKS cluster
aws eks update-kubeconfig --name devops-lab --region us-east-1
kubectl apply -f ../k8s/                     # or: helm upgrade --install devops-lab ../helm/devops-lab
```

> Review `terraform/variables.tf` and set your region, cluster name, and CIDR ranges before applying. Cloud resources cost money — destroy the cluster with `terraform destroy` when you are done.

## Project structure

```
devops-lab/
├── app/                     # FastAPI demo service (/, /health, /metrics)
├── terraform/               # AWS VPC + EKS infrastructure as code
├── k8s/                     # Plain Kubernetes manifests
├── helm/devops-lab/         # Helm chart for the same deployment
├── monitoring/              # Prometheus scrape config + Grafana dashboard
└── docker-compose.yml       # Local full-stack run
```

## Tech stack

Python · FastAPI · Docker · Docker Compose · Terraform · AWS (VPC, EKS) · Kubernetes · Helm · Prometheus · Grafana
