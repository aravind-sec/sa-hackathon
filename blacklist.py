import json

BLACKLIST_FILE = "blacklist.json"


def load_blacklist():
    try:
        with open(BLACKLIST_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_blacklist(data):
    with open(BLACKLIST_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_to_blacklist(ip):
    data = load_blacklist()

    if ip not in data:
        data.append(ip)
        save_blacklist(data)


def remove_from_blacklist(ip):
    data = load_blacklist()

    if ip in data:
        data.remove(ip)
        save_blacklist(data)