import streamlit as st

st.title("📆 Daily Study Plan")

st.info("In future updates, integrate personalized plans via LLM or rule-based scheduler.")
subject = st.selectbox("Subject", ["Physics", "Chemistry", "Math", "Biology"])
topic = st.text_input("Today's Topic")
duration = st.number_input("Time Allotted (hrs)", step=0.5)
if st.button("Add Plan"):
    st.success(f"Study plan added: {subject} - {topic} ({duration} hrs)")
