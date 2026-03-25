import requests
import time

BASE_URL = "http://127.0.0.1:5000"

# -------- Credential Stuffing --------
def credential_stuffing():
    print("Running Credential Stuffing Attack...")
    for i in range(20):
        requests.post(f"{BASE_URL}/login", json={
            "username": "admin",
            "password": f"wrong{i}"
        })
    print("Done.\n")


# -------- Rate Abuse --------
def rate_abuse():
    print("Running Rate Abuse Attack...")
    for i in range(100):
        requests.get(f"{BASE_URL}/api/data")
    print("Done.\n")

# -------- Bot Activity --------


# -------- Suspicious Access --------
def suspicious_access():
    print("Running Suspicious Endpoint Access...")
    for i in range(10):
        requests.get(f"{BASE_URL}/admin")
    print("Done.\n")


# -------- MENU --------
def menu():
    while True:
        print("\nSelect Attack:")
        print("1. Credential Stuffing")
        print("2. Rate Abuse")
        print("3. Suspicious Access")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            credential_stuffing()
        elif choice == "2":
            rate_abuse()
        elif choice == "3":
            suspicious_access()
        elif choice == "4":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu()