from flask import Flask, request, g, render_template, redirect
import time
import os
from blacklist import load_blacklist
from db import init_db, insert_log, archive_logs

app = Flask(__name__, template_folder='templates')

# Ensure folders exist
os.makedirs("logs", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Initialize DB
init_db()


# -------- BEFORE REQUEST --------
@app.before_request
def before_request():
    g.start_time = time.time()

    ip = request.remote_addr
    blacklist = load_blacklist()

    if ip in blacklist:
        g.drop = True
        return ("", 204)  # silent drop


# -------- AFTER REQUEST --------
@app.after_request
def after_request(response):

    # 🚫 Skip logging for dropped requests
    if getattr(g, "drop", False):
        return response

    start_time = getattr(g, "start_time", None)

    if start_time:
        response_time = round((time.time() - start_time) * 1000, 2)
    else:
        response_time = 0

    # Handle request body safely
    if request.is_json:
        body = request.get_json(silent=True)
    else:
        body = request.form.to_dict()

    ip = request.remote_addr

    # -------- SAVE LOG --------
    insert_log(
        ip=ip,
        endpoint=request.path,
        method=request.method,
        status_code=response.status_code,
        response_time_ms=response_time,
        body=body,
        blocked=0
    )

    # -------- ROTATION --------
    archive_logs()

    return response


# -------- ROOT --------
@app.route("/", methods=["GET"])
def home():
    return render_template("login.html")


# -------- LOGIN PAGE --------
@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


# -------- LOGIN API --------
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