import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "leads.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            role TEXT NOT NULL,
            tool TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_lead(email, role, tool=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO leads (email, role, tool, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (email, role, tool, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_all_leads():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT email, role, tool, timestamp FROM leads')
    leads = cursor.fetchall()
    conn.close()
    return leads

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
