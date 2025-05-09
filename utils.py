import sqlite3
from datetime import datetime

# ----------------------------
# Database Connection Function
# ----------------------------
def get_db_connection():
    return sqlite3.connect("study_assistant.db", check_same_thread=False)


# ----------------------------
# Initialize All Tables
# ----------------------------
def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    # Notes Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            content TEXT NOT NULL,
            tags TEXT,
            timestamp TEXT NOT NULL
        )
    ''')

    # Daily Logs Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            content TEXT NOT NULL,
            hours REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')

    # DPP Logs Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS dpp_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            score INTEGER NOT NULL,
            accuracy REAL NOT NULL,
            time_taken TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')

    # Mock Tests Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS mock_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            score INTEGER NOT NULL,
            accuracy REAL NOT NULL,
            time_per_question REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


# ----------------------------
# Utility to Get Current Timestamp
# ----------------------------
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

