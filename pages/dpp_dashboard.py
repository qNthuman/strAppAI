import streamlit as st
import pandas as pd
import numpy as np
from utils import get_db_connection

conn = get_db_connection()

st.title("📊 DPP Logs Dashboard")

# Fetch DPP logs data from the database
def fetch_dpp_logs():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dpp_logs")
    return cursor.fetchall()

dpp_data = fetch_dpp_logs()

# If data exists, show it
if dpp_data:
    df = pd.DataFrame(dpp_data, columns=["ID", "Topic", "Score", "Accuracy", "Time Taken", "Timestamp"])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    st.dataframe(df)

    # Perform some basic analysis
    st.subheader("Basic Statistics")

    # Calculate mean score and accuracy
    mean_score = np.mean(df["Score"])
    mean_accuracy = np.mean(df["Accuracy"])
    avg_time = np.mean(df["Time Taken"].apply(lambda x: int(x.split("m")[0])*60 + int(x.split("m")[1].split("s")[0])))

    st.write(f"Average Score: {mean_score:.2f}")
    st.write(f"Average Accuracy: {mean_accuracy:.2f}%")
    st.write(f"Average Time Taken per DPP: {avg_time // 60}m {avg_time % 60}s")

    # DPP Logs by Topic
    st.subheader("DPP Logs by Topic")
    topic_counts = df["Topic"].value_counts()
    st.bar_chart(topic_counts)
else:
    st.write("No DPP logs found.")
