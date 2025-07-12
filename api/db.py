import sqlite3
from pathlib import Path

DB_FILE = "metrics.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        method TEXT,
        path TEXT,
        status_code INTEGER,
        process_time REAL
    );
    """)
    conn.commit()
    conn.close()

def insert_metric(timestamp, method, path, status_code, process_time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO metrics (timestamp, method, path, status_code, process_time)
        VALUES (?, ?, ?, ?, ?)
    """, (timestamp, method, path, status_code, process_time))
    conn.commit()
    conn.close()

def get_metrics_summary():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*), SUM(process_time), AVG(process_time) FROM metrics
    """)
    result = cursor.fetchone()
    conn.close()
    return {
        "total_requests": result[0] or 0,
        "total_latency": result[1] or 0.0,
        "avg_latency": result[2] or 0.0,
    }
def get_metrics_detailed(limit=100):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, method, path, status_code, process_time
        FROM metrics
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    # Converte em lista de dicionários
    result = []
    for row in rows:
        result.append({
            "timestamp": row[0],
            "method": row[1],
            "path": row[2],
            "status_code": row[3],
            "process_time": row[4]
        })
    return result
