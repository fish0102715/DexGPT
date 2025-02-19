from flask import Flask, request, jsonify, render_template
import sqlite3
import json

app = Flask(__name__)

# Load bot configuration
with open("config.json", "r") as f:
    CONFIG = json.load(f)

# Database connection
def get_db_connection():
    conn = sqlite3.connect("tokens.db")
    conn.row_factory = sqlite3.Row
    return conn

# API: Get latest token trades
@app.route("/api/trades", methods=["GET"])
def get_trades():
    conn = get_db_connection()
    trades = conn.execute("SELECT * FROM tokens ORDER BY created_at DESC LIMIT 50").fetchall()
    conn.close()
    return jsonify([dict(trade) for trade in trades])

# API: Get bot settings
@app.route("/api/config", methods=["GET"])
def get_config():
    return jsonify(CONFIG)

# API: Update bot settings
@app.route("/api/config", methods=["POST"])
def update_config():
    new_config = request.json
    with open("config.json", "w") as f:
        json.dump(new_config, f, indent=4)
    return jsonify({"message": "Settings updated successfully"})

# API: Get latest alerts
@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    conn = get_db_connection()
    alerts = conn.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 20").fetchall()
    conn.close()
    return jsonify([dict(alert) for alert in alerts])

# Serve Frontend UI
@app.route("/")
def dashboard():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
