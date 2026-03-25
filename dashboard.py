from flask import Flask, render_template, request, redirect
import json
from detection import detect_attacks, load_alerts, save_alerts
from risk_scorer import calculate_risk
from blacklist import load_blacklist, save_blacklist
from whitelist import add_to_whitelist

app = Flask(__name__)

def load_logs():
    logs = []
    try:
        with open("logs/requests.log", "r") as f:
            for line in f:
                logs.append(json.loads(line))
    except FileNotFoundError:
        pass
    return logs[::-1]  # Latest first

@app.route("/")
def dashboard():
    logs = load_logs()
    alerts = detect_attacks()  # Returns stored + new alerts
    score, level = calculate_risk(alerts)
    blacklisted_ips = load_blacklist()
    
    # Get all IPs from alerts
    alerted_ips = set(alert["ip_address"] for alert in alerts)
    
    # Mark logs with alerted IPs
    for log in logs:
        log["is_alerted"] = log["ip"] in alerted_ips

    return render_template(
        "dashboard.html",
        logs=logs[:10],
        alerts=alerts,
        score=score,
        level=level,
        blacklisted_ips=blacklisted_ips
    )

@app.route("/remove-blacklist", methods=["POST"])
def remove_blacklist():
    ip = request.form.get("ip")
    blacklist = load_blacklist()
    
    if ip in blacklist:
        blacklist.remove(ip)
        save_blacklist(blacklist)
        
        add_to_whitelist(ip)  
    
    # Also remove from alerts if needed
    alerts = load_alerts()
    alerts = [a for a in alerts if a["ip_address"] != ip]
    save_alerts(alerts)
    
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5001)