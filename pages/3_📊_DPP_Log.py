import streamlit as st
from utils import get_db_connection, get_timestamp

st.title("📊 DPP Log")

conn = get_db_connection()
c = conn.cursor()

topic = st.text_input("Topic")
score = st.number_input("Score", step=1)
accuracy = st.slider("Accuracy (%)", 0, 100)
time_taken = st.text_input("Time Taken (e.g., 6m10s)")
if st.button("Add DPP Log"):
    c.execute("INSERT INTO dpp_logs (topic, score, accuracy, time_taken, timestamp) VALUES (?, ?, ?, ?, ?)",
              (topic, score, accuracy, time_taken, get_timestamp()))
    conn.commit()
    st.success("DPP log saved!")
