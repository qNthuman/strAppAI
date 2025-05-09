import streamlit as st
import sqlite3
from datetime import datetime
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import json

# ============================
# Database Setup (SQLite)
# ============================
conn = sqlite3.connect("study_assistant.db", check_same_thread=False)
c = conn.cursor()

def init_db():
    c.execute('''CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY,
                    subject TEXT,
                    content TEXT,
                    tags TEXT,
                    timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS daily_logs (
                    id INTEGER PRIMARY KEY,
                    subject TEXT,
                    content TEXT,
                    hours REAL,
                    timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS dpp_logs (
                    id INTEGER PRIMARY KEY,
                    topic TEXT,
                    score INTEGER,
                    accuracy REAL,
                    time_taken TEXT,
                    timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS mock_tests (
                    id INTEGER PRIMARY KEY,
                    subject TEXT,
                    score INTEGER,
                    accuracy REAL,
                    time_per_question REAL,
                    timestamp TEXT)''')
    conn.commit()

init_db()

# ============================
# LangChain Setup (Without OpenAI API)
# ============================
memory = ConversationBufferMemory(memory_key="chat_history")

# Define custom logic-based responses instead of relying on OpenAI API
def generate_response(query):
    # Simple rules to respond based on input query (can be expanded with more complex rules)
    query = query.lower()
    if "note" in query:
        return "You can view or create notes for Physics, Chemistry, Math, and Biology."
    elif "dpp" in query:
        return "You can add DPP logs, including topics, scores, and accuracy."
    elif "mock test" in query:
        return "You can log mock test scores with accuracy, time per question, and subject."
    elif "logs" in query:
        return "You can view and edit daily logs, including hours spent and topics studied."
    else:
        return "I'm sorry, I couldn't understand your request. Please ask something about notes, logs, DPP, or mock tests."

# ============================
# Streamlit UI
# ============================
st.title("📘 AI Study Assistant – JEE & IAT")

menu = st.sidebar.selectbox("Choose Action", [
    "Create Note", "View Notes", "Daily Log", "DPP Log", "Mock Test Log", "Ask AI", "Export Logs"
])

# ------------------ Notes ------------------
if menu == "Create Note":
    subject = st.selectbox("Subject", ["Physics", "Chemistry", "Math", "Biology"])
    content = st.text_area("Note Content")
    tags = st.text_input("Tags (comma-separated)")
    if st.button("Save Note"):
        c.execute("INSERT INTO notes (subject, content, tags, timestamp) VALUES (?, ?, ?, ?)",
                  (subject, content, tags, str(datetime.now())))
        conn.commit()
        st.success("Note saved successfully.")

if menu == "View Notes":
    c.execute("SELECT * FROM notes")
    rows = c.fetchall()
    for row in rows:
        st.markdown(f"**{row[1]}** - {row[2]}\n_Tags_: {row[3]}\n_{row[4]}_")

# ------------------ Daily Log ------------------
if menu == "Daily Log":
    subject = st.selectbox("Subject", ["Physics", "Chemistry", "Math", "Biology", "General"])
    content = st.text_input("Topics Studied")
    hours = st.number_input("Hours Spent", step=0.25)
    if st.button("Add Log"):
        c.execute("INSERT INTO daily_logs (subject, content, hours, timestamp) VALUES (?, ?, ?, ?)",
                  (subject, content, hours, str(datetime.now())))
        conn.commit()
        st.success("Daily log saved.")

# ------------------ DPP Log ------------------
if menu == "DPP Log":
    topic = st.text_input("Topic")
    score = st.number_input("Score", step=1)
    accuracy = st.slider("Accuracy (%)", 0, 100)
    time_taken = st.text_input("Time Taken (e.g. 6m10s)")
    if st.button("Add DPP Log"):
        c.execute("INSERT INTO dpp_logs (topic, score, accuracy, time_taken, timestamp) VALUES (?, ?, ?, ?, ?)",
                  (topic, score, accuracy, time_taken, str(datetime.now())))
        conn.commit()
        st.success("DPP log saved.")

# ------------------ Mock Test Log ------------------
if menu == "Mock Test Log":
    subject = st.selectbox("Subject", ["Physics", "Chemistry", "Math", "Biology"])
    score = st.number_input("Score")
    accuracy = st.slider("Accuracy (%)", 0, 100)
    time_per_q = st.number_input("Time per Question (seconds)")
    if st.button("Add Mock Log"):
        c.execute("INSERT INTO mock_tests (subject, score, accuracy, time_per_question, timestamp) VALUES (?, ?, ?, ?, ?)",
                  (subject, score, accuracy, time_per_q, str(datetime.now())))
        conn.commit()
        st.success("Mock test log saved.")

# ------------------ AI Chat ------------------
if menu == "Ask AI":
    query = st.text_input("Ask the Assistant anything about your study logs")
    if st.button("Submit") and query:
        result = generate_response(query)  # Use custom logic to generate response
        st.write(result)

# ------------------ Export ------------------
if menu == "Export Logs":
    st.markdown("Download JSON of notes + logs")
    c.execute("SELECT * FROM notes"); notes = c.fetchall()
    c.execute("SELECT * FROM daily_logs"); logs = c.fetchall()
    c.execute("SELECT * FROM dpp_logs"); dpps = c.fetchall()
    c.execute("SELECT * FROM mock_tests"); mocks = c.fetchall()

    all_data = {
        "notes": notes,
        "daily_logs": logs,
        "dpp_logs": dpps,
        "mock_tests": mocks
    }
    st.download_button("Download JSON", data=json.dumps(all_data, indent=2), file_name="study_logs.json")
