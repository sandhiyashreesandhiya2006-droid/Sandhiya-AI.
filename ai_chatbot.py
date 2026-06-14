import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
import time
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import requests


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

SERPER_API_KEY = st.secrets["SERPER_API_KEY"]

model = genai.GenerativeModel("gemini-2.5-flash")

def search_google(query):

    url = "https://google.serper.dev/search"

    payload = {
        "q": query
    }

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    return response.json()

# =========================
# TITLE
# =========================

st.markdown(
    """
    <div style='text-align:center;'>
        <h1 style='color:#4F46E5;'>🤖 Sandhiya AI</h1>
        <h3>Created by Sandhiya Shree</h3>
        <h4 style='color:#333333;'>
            ✨ Powered by AI, Crafted by Sandhiya Shree ✨
        </h4>
    </div>
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
    st.image("logo.png", width=180)

    st.markdown("### 🤖 Sandhiya AI")
   
    uploaded_file = st.file_uploader(
    "📎 Upload File",
    type=["csv", "xlsx", "pdf", "docx", "txt"]
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

if uploaded_file is not None:

    try:

        if uploaded_file.name.endswith(".csv"):

            df = pd.read_csv(uploaded_file)

            text_content = df.head(20).to_string()

            rows = df.shape[0]
            cols = df.shape[1]
            missing = df.isnull().sum().sum()

            st.markdown("### 📄 Dataset Summary")
            st.write(f"📊 Rows: {rows}")
            st.write(f"📊 Columns: {cols}")
            st.write(f"⚠️ Missing Values: {missing}")

            st.dataframe(df.head())

        elif uploaded_file.name.endswith(".xlsx"):

            df = pd.read_excel(uploaded_file)

            text_content = df.head(20).to_string()

            rows = df.shape[0]
            cols = df.shape[1]
            missing = df.isnull().sum().sum()

            st.markdown("### 📄 Dataset Summary")
            st.write(f"📊 Rows: {rows}")
            st.write(f"📊 Columns: {cols}")
            st.write(f"⚠️ Missing Values: {missing}")

            st.dataframe(df.head())

        elif uploaded_file.name.endswith(".txt"):

            text_content = uploaded_file.read().decode("utf-8")

        elif uploaded_file.name.endswith(".pdf"):

            pdf = PdfReader(uploaded_file)

            text_content = ""

            for page in pdf.pages:
                text_content += page.extract_text() or ""

        elif uploaded_file.name.endswith(".docx"):

            doc = Document(uploaded_file)

            text_content = "\n".join(
                [p.text for p in doc.paragraphs]
            )

        summary_prompt = f"""
Give:

1. Short Summary
2. Important Points
3. Key Information

Content:

{text_content[:5000]}
"""

        summary_response = model.generate_content(summary_prompt)

        st.markdown("### 🤖 AI Summary")
        st.write(summary_response.text)

    except Exception:
        st.warning(
        "⚠️ AI Summary temporarily unavailable. Please try again later."
    )

  
# =========================

# USER INPUT

# =========================

user_input = st.chat_input("Ask anything...")

if user_input:

    st.session_state.messages.append(
    {"role": "user", "content": user_input}
)

    with st.chat_message("user"):
        st.markdown(user_input)

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
5. Be friendly and helpful.
6. Give detailed answers when required.

User Question:
{user_input}
"""

    current_keywords = [
    "cm",
    "chief minister",
    "pm",
    "prime minister",
    "president",
    "minister",
    "latest news",
    "today news",
    "current affairs",
    "election"
]

    try:

        with st.spinner("🤖 Sandhiya AI is thinking..."):

            if any(word in user_input.lower() for word in current_keywords):

            search_result = search_google(user_input)

            response = model.generate_content(
                f"""

Question:
{user_input}

Search Results:
{search_result}

Give the latest and accurate answer.
"""
)

            else:

            response = model.generate_content(prompt)

        answer = response.text

    except Exception:

        answer = """

⚠️ Sandhiya API limit reached.

Please wait for a minute and try again.

This happens when too many requests are sent in a short time.
"""

    st.session_state.messages.append(
    {"role": "assistant", "content": answer}
)

    with st.chat_message("assistant"):
        st.markdown(answer)






    

  
  
 

