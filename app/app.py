import logging
import time
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request

logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.after_request
def log_request(response):
    logger.info(
        "%s %s %s",
        request.method,
        request.path,
        response.status_code,
    )
    return response


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return "This is the about page."


@app.route("/health")
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()})


@app.route("/api/greet", methods=["POST"])
def greet():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "World")
    return jsonify({"message": f"Hello, {name}!"})


@app.route("/api/echo", methods=["POST"])
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify({"echo": data})


@app.route("/api/timestamp")
def timestamp():
    now = datetime.now(timezone.utc)
    return jsonify({
        "utc": now.isoformat(),
        "unix": int(now.timestamp()),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
