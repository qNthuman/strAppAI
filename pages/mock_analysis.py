import streamlit as st
import sqlite3
import pandas as pd
import numpy as np

# Database setup
conn = sqlite3.connect("study_assistant.db", check_same_thread=False)
c = conn.cursor()

def get_mock_tests():
    c.execute("SELECT * FROM mock_tests")
    rows = c.fetchall()
    return rows

# Data Analysis Functions
def analyze_mock_tests(mock_tests):
    data = pd.DataFrame(mock_tests, columns=["ID", "Subject", "Score", "Accuracy", "Time per Question", "Timestamp"])
    average_score = data["Score"].mean()
    average_accuracy = data["Accuracy"].mean()
    average_time = data["Time per Question"].mean()

    return average_score, average_accuracy, average_time

# Mock Test Analysis Page UI
st.header("Mock Test Analysis")

# Fetch and display mock test logs
mock_tests = get_mock_tests()
if mock_tests:
    avg_score, avg_accuracy, avg_time = analyze_mock_tests(mock_tests)
    st.write(f"Average Score: {avg_score:.2f}")
    st.write(f"Average Accuracy: {avg_accuracy:.2f}%")
    st.write(f"Average Time per Question: {avg_time:.2f} seconds")

    # Display mock test data as a DataFrame
    st.subheader("Mock Test Logs")
    df = pd.DataFrame(mock_tests, columns=["ID", "Subject", "Score", "Accuracy", "Time per Question", "Timestamp"])
    st.write(df)
else:
    st.write("No mock test records available.")
