# 🛡️ API Shield — Real-Time API Abuse Detection System

## 📌 Overview

API Shield is a lightweight system that monitors API traffic, detects malicious behavior, and responds in real-time.

It identifies attacks such as:
- Credential stuffing
- Rate abuse
- Bot activity
- Suspicious endpoint access

The system logs requests, analyzes patterns, generates alerts, and blocks malicious IPs — simulating a basic SOC (Security Operations Center) pipeline.

---

## ⚙️ How to Run

### Install Dependencies

```bash
pip install flask
```
### Terminal 1
```bash
python app.py
```

### Terminal 2
```bash
python dashboard.py
```

### Terminal 1
```bash
python simulator_gui.py
```  
