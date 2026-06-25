# Flask App with Docker

A Flask web application containerized with Docker, with a GitHub Actions CI pipeline and GitOps deployment to Kubernetes via ArgoCD.

## Project Structure

```
cicd-demo-app/
├── app/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies (Flask, Gunicorn)
│   ├── Dockerfile          # Container build instructions
│   └── templates/
│       └── index.html      # Interactive home page
├── deployment/
│   ├── deployment.yaml     # Kubernetes Deployment (3 replicas)
│   └── service.yaml        # Kubernetes ClusterIP Service
├── argocd/
│   └── application.yaml    # ArgoCD Application manifest
└── .github/
    └── workflows/
        └── ci.yaml         # GitHub Actions CI pipeline
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Interactive home page |
| `GET` | `/about` | Plain-text about page |
| `GET` | `/health` | Health check — returns status and UTC timestamp |
| `GET` | `/api/timestamp` | Current time in ISO and Unix formats |
| `POST` | `/api/greet` | Returns a personalised greeting |
| `POST` | `/api/echo` | Echoes back any JSON payload |

## Running Locally

**Without Docker:**

```bash
cd app
pip install -r requirements.txt
python app.py
```

**With Docker:**

```bash
docker build -t flask-app ./app
docker run -p 5000:5000 flask-app
```

Visit `http://localhost:5000` — the home page has interactive cards for every endpoint.

## API Usage

**Health check:**

```bash
curl http://localhost:5000/health
```

```json
{"status": "ok", "timestamp": "2025-01-01T12:00:00+00:00"}
```

**Greet:**

```bash
curl -X POST http://localhost:5000/api/greet \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'
```

```json
{"message": "Hello, Alice!"}
```

**Echo:**

```bash
curl -X POST http://localhost:5000/api/echo \
  -H "Content-Type: application/json" \
  -d '{"foo": "bar"}'
```

```json
{"echo": {"foo": "bar"}}
```

**Timestamp:**

```bash
curl http://localhost:5000/api/timestamp
```

```json
{"utc": "2025-01-01T12:00:00+00:00", "unix": 1735732800}
```

## Continuous Integration

The GitHub Actions workflow (`.github/workflows/ci.yaml`) runs on every push and PR to `main` with two sequential jobs:

1. **Lint** — runs `flake8` against `app/`, failing on syntax errors and undefined names.
2. **Docker Build** — builds the image, smoke-tests it with `curl`, then pushes to Docker Hub (`ermin700/flask-app:latest`) **only on direct pushes to `main`**.

Required repository secrets: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`.

## Kubernetes & GitOps

### ArgoCD

The `argocd/application.yaml` manifest configures ArgoCD to watch the `deployment/` directory on the `main` branch and automatically sync changes to the `flask-app` namespace (with prune and self-heal enabled).

Apply the ArgoCD application once:

```bash
kubectl apply -f argocd/application.yaml
```

After that, any change to `deployment/` merged to `main` is automatically rolled out.

### Manual kubectl deploy

```bash
kubectl apply -f deployment/
kubectl get pods -l app=flask-app
kubectl get service flask-app
```

### Accessing the app

The Service is `ClusterIP` (internal only). To reach it locally:

```bash
kubectl port-forward service/flask-app 8080:80
```

Then visit `http://localhost:8080`.

For external access, change the Service `type` to `LoadBalancer` or add an `Ingress` resource.
