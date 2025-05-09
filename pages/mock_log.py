import streamlit as st
from utils import get_db_connection
from datetime import datetime

conn = get_db_connection()

st.title("📋 Mock Test Log")

# Function to add mock test log
def add_mock_log():
    subject = st.selectbox("Subject", ["Physics", "Chemistry", "Math", "Biology"])
    score = st.number_input("Score", min_value=0)
    accuracy = st.number_input("Accuracy (%)", min_value=0, max_value=100)
    time_per_question = st.number_input("Time per Question (seconds)", min_value=0)
    
    if st.button("Save Mock Test Log"):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO mock_tests (subject, score, accuracy, time_per_question, timestamp) VALUES (?, ?, ?, ?, ?)",
                       (subject, score, accuracy, time_per_question, str(datetime.now())))
        conn.commit()
        st.success("Mock test log saved successfully.")

# Function to view mock test logs
def view_mock_logs():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mock_tests")
    rows = cursor.fetchall()
    for row in rows:
        st.markdown(f"**{row[1]}** - Score: {row[2]} - Accuracy: {row[3]}% - Time: {row[4]} seconds - {row[5]}")

# Select action for Mock Test Log
action = st.selectbox("Choose an action", ["Add Mock Test Log", "View Mock Test Logs"])

if action == "Add Mock Test Log":
    add_mock_log()
elif action == "View Mock Test Logs":
    view_mock_logs()
