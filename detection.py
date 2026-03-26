import json
from collections import defaultdict
from datetime import datetime, timedelta
from blacklist import add_to_blacklist
from whitelist import load_whitelist
from db import get_logs   # ✅ DB instead of file

ALERTS_FILE = "logs/alerts.json"


def load_alerts():
    try:
        with open(ALERTS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_alerts(alerts):
    import os
    os.makedirs("logs", exist_ok=True)
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f, indent=2)


def parse_time(ts):
    # ✅ Handles ISO timestamp
    return datetime.fromisoformat(ts)


def detect_attacks():
    logs = get_logs(500)   # ✅ fetch from DB
    stored_alerts = load_alerts()
    whitelist = load_whitelist()

    alerted_ips = set(alert["ip_address"] for alert in stored_alerts)

    ip_requests = defaultdict(list)
    new_alerts = []

    # Group logs by IP
    for log in logs:
        ip_requests[log["ip"]].append(log)

    for ip, entries in ip_requests.items():

        # 🚀 Skip whitelist
        if ip in whitelist:
            continue

        # Skip already alerted
        if ip in alerted_ips:
            continue

        # Sort logs by time
        entries.sort(key=lambda x: x["timestamp"])

        # ========== CREDENTIAL STUFFING ==========
        failed_logins = [
            e for e in entries
            if e["endpoint"] == "/login" and e["status_code"] == 401
        ]

        if len(failed_logins) >= 5:
            new_alerts.append({
                "ip_address": ip,
                "attack_type": "Credential Stuffing",
                "risk_score": 9.0,
                "timestamp": datetime.utcnow().isoformat()
            })
            add_to_blacklist(ip)
            continue

        # ========== RATE ABUSE ==========
        time_window = timedelta(seconds=60)

        for i in range(len(entries)):
            start_time = parse_time(entries[i]["timestamp"])
            count = 1

            for j in range(i + 1, len(entries)):
                current_time = parse_time(entries[j]["timestamp"])

                if current_time - start_time <= time_window:
                    count += 1
                else:
                    break

            if count >= 50:
                new_alerts.append({
                    "ip_address": ip,
                    "attack_type": "Rate Abuse",
                    "risk_score": 8.5,
                    "timestamp": datetime.utcnow().isoformat()
                })
                add_to_blacklist(ip)
                break

        # ========== BOT ACTIVITY (NEW 🔥) ==========
        if len(entries) > 20:
            time_diff = parse_time(entries[-1]["timestamp"]) - parse_time(entries[0]["timestamp"])

            if time_diff.total_seconds() < 5:
                new_alerts.append({
                    "ip_address": ip,
                    "attack_type": "Bot Activity",
                    "risk_score": 9.5,
                    "timestamp": datetime.utcnow().isoformat()
                })
                add_to_blacklist(ip)
                continue

        # ========== SUSPICIOUS ENDPOINT ==========
        admin_hits = [
            e for e in entries
            if e["endpoint"] == "/admin"
        ]

        if len(admin_hits) >= 3:
            new_alerts.append({
                "ip_address": ip,
                "attack_type": "Suspicious Endpoint Access",
                "risk_score": 7.0,
                "timestamp": datetime.utcnow().isoformat()
            })
            add_to_blacklist(ip)

    # Merge alerts
    all_alerts = stored_alerts + new_alerts
    save_alerts(all_alerts)

    return all_alerts


if __name__ == "__main__":
    results = detect_attacks()
    print("\nDetected Alerts:")
    for r in results:
        print(r)