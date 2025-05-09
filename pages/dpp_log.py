import streamlit as st
from utils import get_db_connection
from datetime import datetime

conn = get_db_connection()

st.title("📝 DPP Log")

# Function to add DPP log
def add_dpp_log():
    topic = st.text_input("DPP Topic")
    score = st.number_input("Score", min_value=0)
    accuracy = st.number_input("Accuracy (%)", min_value=0, max_value=100)
    time_taken = st.text_input("Time Taken (e.g., 15m 20s)")
    
    if st.button("Save DPP Log"):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dpp_logs (topic, score, accuracy, time_taken, timestamp) VALUES (?, ?, ?, ?, ?)",
                       (topic, score, accuracy, time_taken, str(datetime.now())))
        conn.commit()
        st.success("DPP log saved successfully.")

# Function to view DPP logs
def view_dpp_logs():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dpp_logs")
    rows = cursor.fetchall()
    for row in rows:
        st.markdown(f"**{row[1]}** - Score: {row[2]} - Accuracy: {row[3]}% - Time: {row[4]} - {row[5]}")

# Select action for DPP Log
action = st.selectbox("Choose an action", ["Add DPP Log", "View DPP Logs"])

if action == "Add DPP Log":
    add_dpp_log()
elif action == "View DPP Logs":
    view_dpp_logs()
