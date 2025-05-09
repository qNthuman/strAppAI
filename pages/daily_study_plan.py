import streamlit as st
import sqlite3
from datetime import datetime, timedelta

# Database setup
conn = sqlite3.connect("study_assistant.db", check_same_thread=False)
c = conn.cursor()

def get_daily_logs():
    c.execute("SELECT * FROM daily_logs")
    rows = c.fetchall()
    return rows

# Daily Study Plan Page UI
st.header("Daily Study Plan")

# Define the study plan based on the logs
def generate_study_plan(logs):
    today = datetime.now().date()
    study_plan = {}
    
    for log in logs:
        log_date = datetime.strptime(log[4], "%Y-%m-%d %H:%M:%S").date()
        if log_date == today:
            subject = log[1]
            study_plan[subject] = study_plan.get(subject, 0) + log[3]
    
    return study_plan

# Generate today's study plan
daily_logs = get_daily_logs()
study_plan = generate_study_plan(daily_logs)

# Display today's study plan
st.write("Today's Study Plan:")
if study_plan:
    for subject, hours in study_plan.items():
        st.write(f"{subject}: {hours} hours")
else:
    st.write("No study logs for today. Please add a daily log.")
