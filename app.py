from flask import Flask, request, g, render_template
import time
import json
import os
from blacklist import load_blacklist

app = Flask(__name__)

LOG_FILE = "logs/requests.log"

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)


# -------- BEFORE REQUEST --------
@app.before_request
def before_request():
    g.start_time = time.time()

    ip = request.remote_addr
    blacklist = load_blacklist()

    if ip in blacklist:
        return {"error": "IP Blacklisted"}, 403


# -------- AFTER REQUEST --------
@app.after_request
def after_request(response):
    start_time = getattr(g, "start_time", None)

    if start_time:
        response_time = round((time.time() - start_time) * 1000, 2)
    else:
        response_time = 0

    # Handle both JSON and form safely
    if request.is_json:
        body = request.get_json(silent=True)
    else:
        body = request.form.to_dict()

    log = {
        "ip": request.remote_addr,
        "endpoint": request.path,
        "method": request.method,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status_code": response.status_code,
        "response_time_ms": response_time,
        "body": body,
        "blocked": request.remote_addr in load_blacklist()
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log) + "\n")

    return response


# -------- LOGIN PAGE (GET) --------
@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


# -------- LOGIN API (POST) --------
@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        data = request.json
    else:
        data = request.form

    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "1234":
        return {"status": "success"}, 200
    else:
        return {"status": "fail"}, 401


# -------- OTHER ENDPOINTS --------
@app.route("/api/data", methods=["GET"])
def get_data():
    return {"data": "Some normal API response"}, 200


@app.route("/admin", methods=["GET"])
def admin():
    return {"message": "Admin panel access"}, 200


# -------- RUN --------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)