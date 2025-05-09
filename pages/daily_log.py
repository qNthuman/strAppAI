import streamlit as st
import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect("study_assistant.db", check_same_thread=False)
c = conn.cursor()

# Daily Log Entry
def add_daily_log(subject, content, hours):
    c.execute("INSERT INTO daily_logs (subject, content, hours, timestamp) VALUES (?, ?, ?, ?)",
              (subject, content, hours, str(datetime.now())))
    conn.commit()

def show_daily_logs():
    c.execute("SELECT * FROM daily_logs")
    rows = c.fetchall()
    return rows

# Daily Log Page UI
st.header("Daily Log")

# Add Daily Log
subject = st.selectbox("Subject", ["Physics", "Chemistry", "Math", "Biology", "General"])
content = st.text_input("Topics Studied")
hours = st.number_input("Hours Spent", step=0.25)

if st.button("Add Log"):
    add_daily_log(subject, content, hours)
    st.success("Daily log saved.")

# View Logs
st.subheader("View All Logs")
logs = show_daily_logs()
for log in logs:
    st.markdown(f"**{log[1]}** - {log[2]}\n_Topics Studied_: {log[3]}\n_Hours Spent_: {log[4]}")
