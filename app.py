from flask import Flask, request, jsonify
import time

app = Flask(__name__)
players = {}

@app.route("/register")
def register():
    import json
    data = json.loads(request.args.get("data", "{}"))
    data["timestamp"] = time.time()
    players[str(data.get("userId"))] = data
    return "ok"

@app.route("/active-users")
def active_users():
    now = time.time()
    active = [p for p in players.values() if now - p.get("timestamp", 0) < 300]
    return jsonify(active)

app.run(host="0.0.0.0", port=8080)
