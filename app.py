from flask import Flask, request, jsonify
import time
import threading

app = Flask(__name__)
players = {}

SECRET_KEY = "yourSecretKey123"

def check_key():
    return request.args.get("key") == SECRET_KEY

# Auto cleanup every 5 seconds
def cleanup():
    while True:
        now = time.time()
        to_remove = [uid for uid, p in players.items() if now - p.get("timestamp", 0) > 15]
        for uid in to_remove:
            del players[uid]
        time.sleep(5)

threading.Thread(target=cleanup, daemon=True).start()

@app.route("/register")
def register():
    if not check_key(): return "unauthorized", 403
    import json
    data = json.loads(request.args.get("data", "{}"))
    data["timestamp"] = time.time()
    players[str(data.get("userId"))] = data
    return "ok"

@app.route("/heartbeat")
def heartbeat():
    if not check_key(): return "unauthorized", 403
    userId = request.args.get("userId", "")
    if userId in players:
        players[userId]["timestamp"] = time.time()
    return "ok"

@app.route("/unregister")
def unregister():
    if not check_key(): return "unauthorized", 403
    userId = request.args.get("userId", "")
    if userId in players:
        del players[userId]
    return "ok"

@app.route("/active-users")
def active_users():
    if not check_key(): return "unauthorized", 403
    now = time.time()
    active = [p for p in players.values() if now - p.get("timestamp", 0) < 15]
    return jsonify(active)

@app.route("/count")
def count():
    if not check_key(): return "unauthorized", 403
    now = time.time()
    active = [p for p in players.values() if now - p.get("timestamp", 0) < 15]
    return jsonify({"count": len(active)})

app.run(host="0.0.0.0", port=8080)
