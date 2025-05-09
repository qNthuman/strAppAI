
import streamlit as st
from utils import init_db
import streamlit as st

st.set_page_config(page_title="JEE & IAT AI Assistant", layout="wide")

st.sidebar.title("📚 Study Assistant")
st.sidebar.markdown("Navigate using the sidebar menu.")
st.sidebar.info("Use the top-left menu to switch pages.")

st.title("📌 Welcome to the JEE + IAT AI Assistant")
st.markdown("""
This assistant helps you:
- 📝 Take notes
- 🗓 Log your daily study activities
- 📊 Track DPPs
- 🧪 Record mock test scores
- 📈 Analyze your preparation
- 📆 Plan your study schedule

Use the sidebar or the navigation menu to get started.
""")



init_db()

st.title("📘 AI Study Assistant – JEE & IAT")
st.markdown("Use the sidebar to navigate across Notes, Logs, Dashboard, and Study Plan.")

