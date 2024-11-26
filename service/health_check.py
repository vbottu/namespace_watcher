from flask import Flask, jsonify
from threading import Thread

# Flask app for health checks
app = Flask(__name__)

# Readiness flag
service_state = None

@app.route("/health", methods=["GET"])
def health():
    # Liveness endpoint, returns 200 to indicate the server is healthy
    return jsonify({"status": "ok"}), 200

@app.route("/readiness", methods=["GET"])
def readiness():
   # Readiness endpoint, returns 200 if the service is ready , else returns 503
    if service_state and service_state.is_ready():
        return jsonify({"status": "ready"}), 200
    return jsonify({"status": "not ready"}), 503

def start_health_server(state):
    global service_state
    service_state = state
    # Starts flask server in a separate thread
    app.run(host="0.0.0.0", port=5000)
