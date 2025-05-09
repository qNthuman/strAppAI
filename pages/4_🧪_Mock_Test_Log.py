import streamlit as st
from utils import get_db_connection, get_timestamp

st.title("🧪 Mock Test Log")

conn = get_db_connection()
c = conn.cursor()

subject = st.selectbox("Subject", ["Physics", "Chemistry", "Math", "Biology"])
score = st.number_input("Score", step=1)
accuracy = st.slider("Accuracy (%)", 0, 100)
time_per_q = st.number_input("Time per Question (seconds)", step=1.0)
if st.button("Add Mock Log"):
    c.execute("INSERT INTO mock_tests (subject, score, accuracy, time_per_question, timestamp) VALUES (?, ?, ?, ?, ?)",
              (subject, score, accuracy, time_per_q, get_timestamp()))
    conn.commit()
    st.success("Mock test log saved!")
    
