# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
# Local (no Docker)
cd app && pip install -r requirements.txt && python app.py
# Visit http://127.0.0.1:5000

# With Docker
docker build -t my-flask-app ./app
docker run -p 5000:5000 my-flask-app
```

## Linting

```bash
cd app
pip install flake8
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics   # hard errors only
flake8 . --count --exit-zero --max-line-length=100 --statistics        # style warnings
```

## Architecture

This is a GitOps CI/CD demo with three layers:

1. **App** (`app/`) — Flask app with three routes (`GET /`, `GET /about`, `POST /api/greet`). No database. Runs on port 5000.

2. **CI** (`.github/workflows/ci.yaml`) — Triggers on pushes/PRs to `main`. Two sequential jobs:
   - `lint`: runs flake8 against `app/`
   - `docker-build`: builds `ermin700/flask-app:latest`, smoke-tests it, then pushes to Docker Hub **only on direct pushes to `main`** (not PRs). Requires `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets.

3. **GitOps / Kubernetes** (`deployment/`, `argocd/`) — ArgoCD watches the `deployment/` directory on the `main` branch and auto-syncs (with prune + self-heal) to the `flask-app` namespace on the in-cluster server. The Deployment runs 3 replicas of `ermin700/flask-app:latest` with `imagePullPolicy: Always`, pulling via the `dockerhub-pull-secret` secret. A `ClusterIP` Service exposes port 80 → 5000.

**Update flow:** push code → CI lints → CI builds & pushes image → update `deployment/deployment.yaml` image tag → ArgoCD detects change and rolls out.
