from flask import Flask, render_template, request, redirect
from detection import detect_attacks, load_alerts, save_alerts
from risk_scorer import calculate_risk
from blacklist import load_blacklist, save_blacklist
from whitelist import add_to_whitelist
from db import get_logs   # ✅ NEW
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def dashboard():
    # ✅ FETCH LOGS FROM DB
    logs = get_logs(200)

    # Fix timestamp format for UI
    for log in logs:
        if "timestamp" in log:
            try:
                dt = datetime.fromisoformat(log["timestamp"])
                log["time"] = dt.strftime("%d %b %H:%M:%S")
            except:
                log["time"] = "N/A"
            
    # Detection + alerts
    alerts = detect_attacks()
    score, level = calculate_risk(alerts)

    blacklisted_ips = load_blacklist()

    # Mark alerted logs
    alerted_ips = set(alert["ip_address"] for alert in alerts)

    for log in logs:
        log["is_alerted"] = log["ip"] in alerted_ips

    return render_template(
        "dashboard.html",
        logs=logs,
        alerts=alerts,
        score=score,
        level=level,
        blacklisted_ips=blacklisted_ips
    )


@app.route("/remove-blacklist", methods=["POST"])
def remove_blacklist_route():
    ip = request.form.get("ip")
    blacklist = load_blacklist()

    if ip in blacklist:
        blacklist.remove(ip)
        save_blacklist(blacklist)

        # ✅ Add to whitelist (prevents re-blacklisting)
        add_to_whitelist(ip)

    # Remove alerts for clean UI
    alerts = load_alerts()
    alerts = [a for a in alerts if a["ip_address"] != ip]
    save_alerts(alerts)

    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True, port=5001)