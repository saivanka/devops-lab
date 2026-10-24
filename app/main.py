"""DevOps Pipeline Lab demo service.

A tiny FastAPI app used as the deployable artifact for the CI/CD,
Kubernetes, and observability parts of this project. It exposes:
  GET /        - service info
  GET /health  - liveness/readiness probe target
  GET /metrics - Prometheus-compatible metrics (plain text exposition)
"""

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI(title="devops-lab", version="1.0.0")

_REQUESTS = {"total": 0}


@app.get("/")
def root():
    _REQUESTS["total"] += 1
    return {
        "service": "devops-lab",
        "status": "ok",
        "message": "Deployed via CI/CD to Kubernetes.",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return (
        "# HELP devops_lab_requests_total Total requests served.\n"
        "# TYPE devops_lab_requests_total counter\n"
        f"devops_lab_requests_total {_REQUESTS['total']}\n"
    )
