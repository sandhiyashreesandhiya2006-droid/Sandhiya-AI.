import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
import time

# =========================
# PAGE SETTINGS
# =========================
st.set_page_config(
    page_title="Sandhiya AI",
    page_icon="🤖",
    layout="wide"
)

# =========================
# API KEY
# =========================
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

# =========================
# TITLE
# =========================
st.markdown(
    """
    <h1 style='text-align:center;color:#4F46E5;'>
        🤖 Sandhiya AI
    </h1>
    <p style='text-align:center;'>
        Created by Sandhiya Shree
    </p>
    """,
    unsafe_allow_html=True
)

# =========================
# CHAT HISTORY
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


with st.sidebar:
    uploaded_file = st.file_uploader(
        "📎 Upload File"
    )
    
    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.rerun()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    chat_text = "\n\n".join(
        [f"{msg['role']}: {msg['content']}"
         for msg in st.session_state.messages]
    )

    st.download_button(
        "📥 Download Chat",
        chat_text,
        file_name="sandhiya_chat.txt",
        mime="text/plain"
    )
  

# =========================
# USER INPUT
# =========================
user_input = st.chat_input("Ask anything...")

if user_input:

    # User message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Custom prompt
    prompt = f"""
You are Sandhiya AI.

Creator: Sandhiya Shree.

Important Rules:

1. If the user speaks Tamil, answer in Tamil.
2. If the user speaks English, answer in English.
3. If someone asks:
   - Who created you?
   - Who is your creator?
   - Who is your owner?
   - Who developed you?
   - Tell me about your creator

Answer:

"I was created by Sandhiya Shree, a passionate Computer Science student, aspiring Data Analyst, and AI enthusiast."

4. Speak positively about Sandhiya Shree.

Example:

"Sandhiya Shree is a dedicated Computer Science student who is passionate about AI, Data Analytics, Python, Power BI, and technology projects."

5. Be friendly and helpful.
6. Give detailed answers when required.

User Question:
{user_input}
"""



    

  
  
 

