import streamlit as st
from utils import get_db_connection
from datetime import datetime

conn = get_db_connection()

st.title("📚 Notes")

# Function to add notes
def add_note():
    subject = st.selectbox("Subject", ["Physics", "Chemistry", "Math", "Biology"])
    content = st.text_area("Note Content")
    tags = st.text_input("Tags (comma-separated)")
    if st.button("Save Note"):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes (subject, content, tags, timestamp) VALUES (?, ?, ?, ?)",
                       (subject, content, tags, str(datetime.now())))
        conn.commit()
        st.success("Note saved successfully.")

# Function to view notes
def view_notes():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    rows = cursor.fetchall()
    for row in rows:
        st.markdown(f"**{row[1]}** - {row[2]}\n_Tags_: {row[3]}\n_{row[4]}_")

# Select action for Notes
action = st.selectbox("Choose an action", ["Create Note", "View Notes"])

if action == "Create Note":
    add_note()
elif action == "View Notes":
    view_notes()