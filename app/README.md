# Flask App with Docker

A simple Flask web application containerized with Docker.

## Project Structure

```
myapp/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container build instructions
├── .dockerignore       # Files to exclude from the image
└── templates/
    └── index.html      # Home page template
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
