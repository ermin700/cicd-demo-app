# Flask App with Docker

A simple Flask web application containerized with Docker, with CI and
Kubernetes deployment manifests.

## Project Structure

```
myapp/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container build instructions
├── .dockerignore           # Files to exclude from the image
├── deployment.yaml         # Kubernetes Deployment + Service
├── templates/
│   └── index.html          # Home page template
└── .github/
    └── workflows/
        └── ci.yaml         # GitHub Actions CI pipeline
```

## Application

`app.py` defines a Flask app with three routes:

- `GET /` — renders the home page (`index.html`)
- `GET /about` — returns a plain-text about page
- `POST /api/greet` — accepts JSON `{"name": "..."}` and returns a greeting

The app listens on `0.0.0.0:5000` so it's reachable from outside the container.

## Requirements

Dependencies are listed in `requirements.txt`:

```
flask
```

## Running Locally (without Docker)

```bash
pip install -r requirements.txt
python app.py
```

Then visit `http://127.0.0.1:5000`.

## Running with Docker

Build the image:

```bash
docker build -t my-flask-app .
```

Run the container:

```bash
docker run -p 5000:5000 my-flask-app
```

Then visit `http://localhost:5000`. The `-p 5000:5000` flag maps the
container's port 5000 to your machine's port 5000.

## API Usage

Example request to the greet endpoint:

```bash
curl -X POST http://localhost:5000/api/greet \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'
```

Response:

```json
{"message": "Hello, Alice!"}
```

## Continuous Integration

The GitHub Actions workflow at `.github/workflows/ci.yaml` runs on every
push and pull request to `main`. It has two jobs:

1. **Lint** — installs dependencies and runs `flake8`, failing only on real
   errors (syntax errors, undefined names) and reporting style issues as
   non-blocking warnings.
2. **Docker Build** — builds the image, starts the container, and curls the
   home page as a smoke test. Runs only if linting passes.

## Kubernetes Deployment

The `deployment.yaml` manifest defines two resources:

- A **Deployment** running 2 replicas of the app, with CPU/memory
  requests and limits, plus liveness and readiness probes on `/` (port 5000).
- A **Service** (type `ClusterIP`) that exposes the pods internally on
  port 80, forwarding to the container's port 5000.

Apply it with:

```bash
kubectl apply -f deployment.yaml
```

Check the rollout:

```bash
kubectl get pods -l app=flask-app
kubectl get service flask-app
```

### Before deploying

- **Image:** the manifest uses `my-flask-app:latest` with
  `imagePullPolicy: IfNotPresent`, which suits a local cluster (minikube,
  kind) where the image is loaded directly. For a real cluster, push the
  image to a registry and update the `image:` field, e.g.
  `ghcr.io/<your-user>/my-flask-app:1.0.0`. Prefer a pinned version tag
  over `latest` for predictable rollouts.

### Accessing the app

`ClusterIP` only exposes the app inside the cluster. To reach it:

- **Quick local test:**

  ```bash
  kubectl port-forward service/flask-app 8080:80
  ```

  Then visit `http://localhost:8080`.

- **Cloud provider:** change the Service `type` to `LoadBalancer`.
- **Production HTTP:** add an `Ingress` resource in front of the Service.

## Production Notes

The default setup uses Flask's built-in development server, which is not
suitable for production. For a production deployment, use a WSGI server
like Gunicorn:

1. Add `gunicorn` to `requirements.txt`
2. Change the Dockerfile `CMD` to:

   ```dockerfile
   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
   ```

Also set `debug=False` (or remove the `debug` flag) in `app.py` when
deploying.
