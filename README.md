# DevOps Journey — Full CI/CD Pipeline with GitOps 🚀

![CI](https://github.com/vuthin-devops-journey/Setup-DevOps/actions/workflows/ci.yml/badge.svg)

A production-style DevOps pipeline built from scratch: a Flask API backed by
PostgreSQL, containerized, tested in CI, published to a container registry,
deployed to Kubernetes via Helm, continuously delivered with ArgoCD GitOps,
observed with Prometheus/Grafana, and provisioned on AWS with Terraform.

## Architecture
Developer → git push
│
├─ CI (GitHub Actions)
│ ├─ flake8 lint
│ ├─ pytest (8 tests, PostgreSQL service container)
│ ├─ docker build → GHCR (tag = commit SHA)
│ └─ update Helm values.yaml with new tag
│
├─ Git = single source of truth
│
├─ CD (ArgoCD, pull-based GitOps)
│ └─ auto-sync → Kubernetes rolling update (zero downtime)
│
└─ Observability (Prometheus scrape → Grafana dashboards)


## Stack

| Layer | Technology |
|---|---|
| Application | Python 3.12, Flask, PostgreSQL |
| Testing | pytest, flake8 |
| CI/CD | GitHub Actions, ArgoCD |
| Containers | Docker, docker-compose, GHCR |
| Orchestration | Kubernetes (Deployments, Services, Secrets, PVC, probes) |
| Packaging | Helm |
| Monitoring | Prometheus, Grafana, prometheus-flask-exporter |
| Infrastructure | Terraform (AWS: EC2, Security Groups, S3) |

## Endpoints

| Route | Description |
|---|---|
| `/` | Welcome message |
| `/health` | Health check — used by K8s liveness/readiness probes |
| `/version` | Application version |
| `/visits` | Visit counter persisted in PostgreSQL |
| `/metrics` | Prometheus metrics (request counts, latency histograms) |

## Key Implementation Details

- **12-factor config** — all DB settings via environment variables, so the same
  image runs unchanged in local Docker, CI, and Kubernetes
- **Immutable image tags** — images tagged with commit SHA, never `latest`,
  giving full traceability and one-commit rollbacks
- **Pull-based CD** — ArgoCD runs inside the cluster and pulls from Git, so CI
  never needs cluster credentials
- **Self-healing** — ArgoCD reconciles drift; K8s restarts unhealthy pods via
  `/health` probes
- **Zero-downtime deploys** — RollingUpdate with `maxUnavailable: 0`
- **Infrastructure as Code** — EC2 provisioned by Terraform with Docker
  bootstrapped through `user_data`; security groups scoped to the operator's
  current IP, resolved dynamically at plan time

## Repository Layout
.github/workflows/ CI pipeline + Terraform validation
app.py, test_app.py Flask API and pytest suite
Dockerfile Container image build
docker-compose.yml Local dev (app + PostgreSQL)
k8s/ Raw Kubernetes manifests
charts/myapp/ Helm chart (templates + values)
argocd/ ArgoCD Application (GitOps config)
terraform/ AWS infrastructure as code
docs/ Daily engineering notes


## Run Locally

```bash
docker compose up --build
# → http://localhost:5000/health
```

## Run Tests

```bash
python -m venv venv && source venv/Scripts/activate
pip install -r requirements.txt
docker compose up -d db
DB_PORT=5433 pytest -v
```

## Deploy to Kubernetes

```bash
kubectl create secret generic db-secret \
  --from-literal=POSTGRES_DB=devops \
  --from-literal=POSTGRES_USER=devops \
  --from-literal=POSTGRES_PASSWORD=<password>

kubectl apply -f k8s/postgres.yaml
helm upgrade --install myapp charts/myapp
```

## Provision AWS Infrastructure

```bash
cd terraform
terraform init
terraform plan      # review planned changes
terraform apply     # provision EC2 + security group
curl $(terraform output -raw app_url)
terraform destroy   # tear down completely
```

## Engineering Notes

Daily notes covering design decisions and real debugging sessions — port
conflicts, ImagePullBackOff, kubeconfig drift, orphaned Helm releases, SSH
timeouts behind restrictive networks — are in [docs/](docs/).
