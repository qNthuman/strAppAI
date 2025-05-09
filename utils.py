
import sqlite3
from datetime import datetime

def get_db_connection():
    return sqlite3.connect("study_assistant.db", check_same_thread=False)

def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT, content TEXT, tags TEXT, timestamp TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT, content TEXT, hours REAL, timestamp TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS dpp_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT, score INTEGER, accuracy REAL, time_taken TEXT, timestamp TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS mock_tests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT, score INTEGER, accuracy REAL, time_per_question REAL, timestamp TEXT)''')

    conn.commit()
    conn.close()

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```

---

### ✅ `pages/1_📒_Notes.py`
```python
import streamlit as st
from utils import get_db_connection, get_timestamp

st.title("📒 Notes")

conn = get_db_connection()
c = conn.cursor()

subject = st.selectbox("Subject", ["Physics", "Chemistry", "Math", "Biology"])
content = st.text_area("Note Content")
tags = st.text_input("Tags (comma-separated)")
if st.button("Save Note"):
    c.execute("INSERT INTO notes (subject, content, tags, timestamp) VALUES (?, ?, ?, ?)",
              (subject, content, tags, get_timestamp()))
    conn.commit()
    st.success("Note saved successfully!")

st.markdown("---")
c.execute("SELECT * FROM notes")
for row in c.fetchall():
    st.markdown(f"**{row[1]}** — {row[2]}\n_Tags_: {row[3]}\n_{row[4]}")
