import json

WHITELIST_FILE = "whitelist.json"


def load_whitelist():
    try:
        with open(WHITELIST_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_whitelist(data):
    with open(WHITELIST_FILE, "w") as f:
        json.dump(data, f)


def add_to_whitelist(ip):
    data = load_whitelist()
    if ip not in data:
        data.append(ip)
        save_whitelist(data)