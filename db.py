import sqlite3
import os
from datetime import datetime
import json

DB_FILE = "logs/api_logs.db"
ARCHIVE_DB = "logs/api_logs_archive.db"


def init_db():
    os.makedirs("logs", exist_ok=True)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            ip TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            method TEXT NOT NULL,
            status_code INTEGER NOT NULL,
            response_time_ms REAL,
            body TEXT,
            blocked INTEGER DEFAULT 0
        )
    ''')

    # Optional index (faster queries)
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_ip ON logs(ip)')

    conn.commit()
    conn.close()


def insert_log(ip, endpoint, method, status_code, response_time_ms, body, blocked):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    timestamp = datetime.utcnow().isoformat()

    cursor.execute('''
        INSERT INTO logs (timestamp, ip, endpoint, method, status_code, response_time_ms, body, blocked)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        timestamp,
        ip,
        endpoint,
        method,
        status_code,
        response_time_ms,
        json.dumps(body) if body else None,
        int(blocked)
    ))

    conn.commit()
    conn.close()


def get_logs(limit=200):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM logs ORDER BY id DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]


def get_log_count():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM logs')
    count = cursor.fetchone()[0]

    conn.close()
    return count


def archive_logs():
    count = get_log_count()

    if count >= 200:   # ✅ fixed condition

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM logs ORDER BY id ASC LIMIT 100')
        old_logs = cursor.fetchall()

        archive_conn = sqlite3.connect(ARCHIVE_DB)
        archive_cursor = archive_conn.cursor()

        archive_cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs_archive (
                id INTEGER,
                timestamp TEXT,
                ip TEXT,
                endpoint TEXT,
                method TEXT,
                status_code INTEGER,
                response_time_ms REAL,
                body TEXT,
                blocked INTEGER,
                archived_at TEXT
            )
        ''')

        archived_at = datetime.utcnow().isoformat()

        for log in old_logs:
            archive_cursor.execute('''
                INSERT INTO logs_archive VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (*log, archived_at))

        archive_conn.commit()
        archive_conn.close()

        # Delete archived logs from main DB
        cursor.execute('DELETE FROM logs WHERE id IN (SELECT id FROM logs ORDER BY id ASC LIMIT 100)')

        conn.commit()
        conn.close()

        print("✓ Archived 100 logs")