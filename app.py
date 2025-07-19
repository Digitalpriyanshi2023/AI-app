# app.py

import os
import pandas as pd
import streamlit as st
import google.generativeai as genai

# 🔐 Setup your Gemini API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyAEjD-7P2ateq0U0AipxRpy3XgPUKmX6Ww"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# 🌟 Load Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")

# 🎨 Page config
st.set_page_config(page_title="Priyanshi's Excel AI", layout="centered")
st.markdown(
    """
    <style>
    .title {
        font-size: 38px;
        font-weight: 900;
        color: #6a11cb;
        text-align: center;
        margin-bottom: 0.5em;
    }
    .sub {
        font-size: 18px;
        text-align: center;
        color: #333;
        margin-bottom: 2em;
    }
    .footer {
        font-size: 14px;
        text-align: center;
        margin-top: 4em;
        color: #aaa;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 🧠 Title
st.markdown('<div class="title">📊 Priyanshi\'s Gemini Excel Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Upload an Excel file and ask anything about it. Let Gemini AI analyze it for you 💡</div>', unsafe_allow_html=True)

# 📁 Upload Excel file
uploaded_file = st.file_uploader("📂 Upload Excel File", type=["xlsx"])

# 💬 Ask a question
question = st.text_input("💬 Ask your question about the Excel data")

# ✅ Run only if both file and question are provided
if uploaded_file and question:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ File uploaded successfully!")
        st.subheader("📄 Excel Data Preview:")
        st.dataframe(df.head(10), use_container_width=True)

        # Convert full data to CSV text
        csv_data = df.to_csv(index=False)

        # Prepare prompt
        context = f"""
You are a smart assistant helping Priyanshi analyze her computer accessories Excel sheet.

Here is the Excel data in CSV format:

{csv_data}

Please answer this question:
{question}
"""
        # Gemini AI response
        response = model.generate_content(context)
        st.subheader("🤖 Gemini's Answer:")
        st.write(response.text)

    except Exception as e:
        st.error(f"❌ Something went wrong: {e}")

# 👣 Footer
st.markdown('<div class="footer">Made with 💖 by Priyanshi | Powered by Gemini + Streamlit</div>', unsafe_allow_html=True)
