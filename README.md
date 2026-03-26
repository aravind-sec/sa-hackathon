# \# 🛡️ API Shield — Real-Time API Abuse Detection \& Response System

# 

# \## 📌 Overview

# 

# API Shield is a real-time API security system designed to monitor, detect, and respond to malicious activities such as credential stuffing, rate abuse, bot traffic, and suspicious endpoint access.

# 

# It simulates a \*\*mini SOC (Security Operations Center)\*\* pipeline by capturing API traffic, analyzing behavior, generating alerts, and enforcing response mechanisms like IP blacklisting.

# 

# \---

# 

# \## 🚀 Key Features

# 

# \### 🔍 Real-Time Monitoring

# 

# \* Logs all incoming API requests (IP, endpoint, method, status, response time)

# \* Stores logs in \*\*SQLite database\*\* for efficient querying

# 

# \### 🧠 Threat Detection Engine

# 

# Detects:

# 

# \* Credential Stuffing (multiple failed logins)

# \* Rate Abuse (50+ requests/min)

# \* Bot Activity (burst traffic \& endpoint spam)

# \* Suspicious Endpoint Access (`/admin` probing)

# 

# \### ⚡ Automated Response

# 

# \* Automatically \*\*blacklists malicious IPs\*\*

# \* Drops further requests from blacklisted IPs (acts like a firewall)

# 

# \### 📊 Interactive Dashboard

# 

# \* Live logs (real-time updates)

# \* Active alerts

# \* Risk score calculation

# \* Blacklisted IP management

# 

# \### 🔐 Authentication \& Session Protection

# 

# \* Login attempt limiting (prevents brute force)

# \* Session-based authentication

# \* Protected endpoints (`/admin`, `/api/data`)

# \* Logout functionality

# 

# \### 🗄️ Log Management

# 

# \* Logs stored in SQLite DB

# \* Automatic \*\*log rotation after 200 entries\*\*

# \* Old logs archived (not deleted)

# 

# \---

# 

# \## 🏗️ System Architecture

# 

# ```

# Attack Simulator → Flask API → Logging (DB)

# &#x20;                        ↓

# &#x20;                 Detection Engine

# &#x20;                        ↓

# &#x20;             Risk Scoring + Alerts

# &#x20;                        ↓

# &#x20;                  Dashboard UI

# ```

# 

# \---

# 

# \## 🧰 Tech Stack

# 

# \* \*\*Backend:\*\* Python (Flask)

# \* \*\*Database:\*\* SQLite

# \* \*\*Frontend:\*\* HTML, CSS, JavaScript

# \* \*\*Visualization:\*\* Chart.js (optional)

# \* \*\*API Testing:\*\* Postman / Python requests

# \* \*\*Version Control:\*\* GitHub

# 

# \---

# 

# \## 📁 Project Structure

# 

# ```

# api\_defense\_system/

# │

# ├── app.py                # Main API (logging + auth + session)

# ├── dashboard.py         # Dashboard server

# ├── detection.py         # Threat detection engine

# ├── db.py                # Database \& log rotation

# ├── blacklist.py         # Blacklist handling

# ├── whitelist.py         # Whitelist handling

# ├── risk\_scorer.py       # Risk scoring logic

# ├── simulator.py         # Attack simulator

# │

# ├── templates/

# │   └── dashboard.html

# │   └── login.html

# │

# ├── logs/

# │   ├── api\_logs.db

# │   ├── api\_logs\_archive.db

# │   └── alerts.json

# │

# └── README.md

# ```

# 

# \---

# 

# \## ⚙️ How to Run the Project

# 

# \### 1️⃣ Install Requirements

# 

# ```bash

# pip install flask

# ```

# 

# \---

# 

# \### 2️⃣ Start the API Server

# 

# ```bash

# python app.py

# ```

# 

# Runs on:

# 

# ```

# http://127.0.0.1:5000

# ```

# 

# \---

# 

# \### 3️⃣ Start the Dashboard

# 

# ```bash

# python dashboard.py

# ```

# 

# Runs on:

# 

# ```

# http://127.0.0.1:5001

# ```

# 

# \---

# 

# \### 4️⃣ (Optional) Run Attack Simulator

# 

# ```bash

# python simulator.py

# ```

# 

# Simulates:

# 

# \* Credential stuffing

# \* Rate abuse

# \* Bot traffic

# 

# \---

# 

# \## 🔐 Authentication Flow

# 

# 1\. User logs in via `/login`

# 2\. Session is created (`session\["user"]`)

# 3\. Protected endpoints validate session

# 4\. Unauthorized users are blocked

# 

# \---

# 

# \## 🧪 Testing the System

# 

# \### Normal Flow

# 

# \* Login with:

# 

# &#x20; ```

# &#x20; username: admin

# &#x20; password: 1234

# &#x20; ```

# 

# \---

# 

# \### Attack Simulation

# 

# \* Run simulator OR

# \* Send repeated requests manually

# 

# \---

# 

# \### Observe:

# 

# \* Logs updating in dashboard

# \* Alerts being generated

# \* IP getting blacklisted

# \* Requests being dropped

# 

# \---

# 

# \## ⚠️ Notes

# 

# \* Use \*\*http://127.0.0.1:5000\*\* (avoid mixing with `localhost`)

# \* This is a \*\*prototype system\*\*, not production-ready

# \* No password hashing or JWT implemented (by design)

# 

# \---

# 

# \## 🎯 Future Enhancements

# 

# \* JWT-based authentication

# \* Geo-IP enrichment

# \* WebSocket real-time updates

# \* Machine learning-based anomaly detection

# \* Distributed logging (Kafka / ELK stack)

# 

# \---

# 

# \## 👨‍💻 Author

# 

# Built as part of a cybersecurity hackathon project focusing on \*\*API security and abuse detection\*\*.

# 

# \---

# 

# \## 🏁 Conclusion

# 

# API Shield demonstrates how modern systems can:

# 

# \* Monitor API traffic

# \* Detect malicious behavior

# \* Respond in real-time

# 

# Bridging the gap between \*\*detection\*\* and \*\*prevention\*\* in API security.

# 

# \---



