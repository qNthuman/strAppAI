import streamlit as st
from utils import get_db_connection, get_timestamp

st.title("📝 Daily Study Log")

conn = get_db_connection()
c = conn.cursor()

subject = st.selectbox("Subject", ["Physics", "Chemistry", "Math", "Biology", "General"])
topics = st.text_input("Topics Studied")
hours = st.number_input("Hours Spent", min_value=0.0, step=0.25)
if st.button("Add Log"):
    c.execute("INSERT INTO daily_logs (subject, content, hours, timestamp) VALUES (?, ?, ?, ?)",
              (subject, topics, hours, get_timestamp()))
    conn.commit()
    st.success("Daily log saved!")
