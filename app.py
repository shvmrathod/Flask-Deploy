from flask import Flask, render_template, request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import logging

app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)

# Prometheus metrics
REQUEST_COUNT = Counter("request_count", "Total number of requests", ["method", "endpoint"])

@app.route("/", methods=["GET", "POST"])
def home():
    REQUEST_COUNT.labels(method=request.method, endpoint="/").inc()
    message = ""
    if request.method == "POST":
        name = request.form.get("name")
        message = f"Hello {name}, Welcome to the Kubernetes test application!!!"
        app.logger.info(f"Greeting sent to {name}")
    return render_template("index.html", message=message)

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)