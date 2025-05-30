from flask import Flask, jsonify
from kafka_consumer import crypto_data, consume
import threading
import os

app = Flask(__name__)

@app.route("/api/prices", methods=["GET"])
def get_prices():
    return jsonify(crypto_data)

@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    log_path = "alerts.log"
    if not os.path.exists(log_path):
        return jsonify({"alerts": []})

    with open(log_path, "r") as file:
        lines = file.readlines()

    alerts = [line.strip() for line in lines if line.strip()]
    return jsonify({"alerts": alerts})

if __name__ == "__main__":
    thread = threading.Thread(target=consume, daemon=True)
    thread.start()

    app.run(debug=True, port=5000)
