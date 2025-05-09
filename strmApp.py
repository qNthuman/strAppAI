
import streamlit as st
from utils import init_db

st.set_page_config(page_title="JEE & IAT Study Assistant", layout="wide")

init_db()

st.title("📘 AI Study Assistant – JEE & IAT")
st.markdown("Use the sidebar to navigate across Notes, Logs, Dashboard, and Study Plan.")

