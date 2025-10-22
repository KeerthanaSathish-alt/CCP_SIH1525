from flask import Flask, jsonify
from flask_cors import CORS
import random
import threading
import time

app = Flask(__name__)
CORS(app)

# ==============================
# Simulated Data Storage
# ==============================
data = {
    "current": {"energy": 0, "water": 0, "savings": 0, "carbon": 0},
    "previous_day": {"energy": 0, "water": 0},
    "alerts": [],
    "devices": []
}

# Thresholds for generating alerts
ENERGY_THRESHOLD = 350
WATER_THRESHOLD = 80

# ==============================
# Simulation Functions
# ==============================
def simulate_usage():
    """Simulate dynamic usage metrics every 10 seconds"""
    while True:
        data["current"]["energy"] = random.randint(200, 400)
        data["current"]["water"] = random.randint(20, 100)
        data["current"]["savings"] = random.randint(80, 200)
        data["current"]["carbon"] = round(random.uniform(0.5, 5), 1)

        # Previous day metrics
        data["previous_day"]["energy"] = random.randint(200, 350)
        data["previous_day"]["water"] = random.randint(20, 90)

        # Devices usage
        data["devices"] = [
            {"name": "HVAC", "usage": random.randint(20, 50)},
            {"name": "Water Heater", "usage": random.randint(10, 40)},
            {"name": "Appliances", "usage": random.randint(10, 30)},
            {"name": "Lighting", "usage": random.randint(5, 20)},
        ]

        # Alerts
        alerts = []
        if data["current"]["energy"] > ENERGY_THRESHOLD:
            alerts.append({"msg": f"⚠ High Energy Usage: {data['current']['energy']} kWh", "status": "warning"})
        if data["current"]["water"] > WATER_THRESHOLD:
            alerts.append({"msg": f"❌ Water Usage Exceeded: {data['current']['water']} L", "status": "critical"})
        data["alerts"] = alerts

        time.sleep(10)

# Start simulation thread
threading.Thread(target=simulate_usage, daemon=True).start()

# ==============================
# API Endpoints
# ==============================
@app.route("/")
def home():
    return jsonify({"status": "Backend running ✅"})

@app.route("/api/dashboard")
def get_dashboard():
    return jsonify(data["current"])

@app.route("/api/previous-day")
def get_previous_day():
    return jsonify(data["previous_day"])

@app.route("/api/alerts")
def get_alerts():
    return jsonify(data["alerts"])

@app.route("/api/devices")
def get_devices():
    return jsonify(data["devices"])

# ==============================
# Run Server
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
