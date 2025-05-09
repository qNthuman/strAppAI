import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('study_assistant.db', check_same_thread=False)
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    # Create tables if not exist
    c.execute('''CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY,
                    subject TEXT,
                    content TEXT,
                    tags TEXT,
                    timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS daily_logs (
                    id INTEGER PRIMARY KEY,
                    subject TEXT,
                    content TEXT,
                    hours REAL,
                    timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS dpp_logs (
                    id INTEGER PRIMARY KEY,
                    topic TEXT,
                    score INTEGER,
                    accuracy REAL,
                    time_taken TEXT,
                    timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS mock_tests (
                    id INTEGER PRIMARY KEY,
                    subject TEXT,
                    score INTEGER,
                    accuracy REAL,
                    time_per_question REAL,
                    timestamp TEXT)''')
    conn.commit()
    conn.close()
