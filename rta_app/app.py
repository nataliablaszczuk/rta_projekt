from flask import Flask, jsonify
from kafka_consumer import crypto_data

app = Flask(__name__)

@app.route("/api/prices", methods=["GET"])
def get_prices():
    return jsonify(crypto_data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
