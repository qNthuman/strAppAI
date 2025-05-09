# AI Assistant for JEE & IAT Prep with LangChain + Streamlit UI + SQLite

import streamlit as st
import sqlite3
from datetime import datetime
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI

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
# LangChain Setup
# ============================
memory = ConversationBufferMemory()
llm = ChatOpenAI(temperature=0.5)
prompt = PromptTemplate(
    input_variables=["input"],
    template="""
    You are a helpful AI assistant supporting a student preparing for JEE and IAT. 
    Manage these tasks:
    - Subject-wise notes (create, view, edit, delete, tag by topic/chapter)
    - Daily logs (topics studied, DPPs done, hours spent)
    - DPP tracking (topic, score, accuracy, time)
    - Mock test logs (scores, accuracy, trends)
    - Respond to requests like: "Show all notes on Electrostatics" or "Log today's Chemistry study session."
    - Allow deletion, editing, and retrieval of entries.

    Input: {input}
    Output:
    """
)
chain = ConversationChain(llm=llm, memory=memory, prompt=prompt)

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
        result = chain.run(input=query)
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
