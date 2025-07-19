# app.py

import os
import pandas as pd
import streamlit as st
import google.generativeai as genai

# ✅ Gemini API key setup
os.environ["GOOGLE_API_KEY"] = "AIzaSyAEjD-7P2ateq0U0AipxRpy3XgPUKmX6Ww"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# ✅ Load Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")

# ✅ Streamlit UI setup
st.set_page_config(page_title="📊 Gemini Excel Chatbot", layout="centered")
st.title("📊 Gemini Excel Chatbot")
st.markdown("Upload your Excel file and ask questions about it.")

# ✅ Upload section
uploaded_file = st.file_uploader("📁 Upload an Excel file", type=["xlsx"])
question = st.text_input("💬 Ask a question about the file")

# ✅ Response section
if uploaded_file and question:
    try:
        # Read Excel
        df = pd.read_excel(uploaded_file)
        st.write("📄 Excel Preview:")
        st.dataframe(df.head(10))

        # Send full data as CSV
        csv_data = df.to_csv(index=False)

        context = f"""
You are a smart data analyst assistant.
Here is the Excel data in CSV format:

{csv_data}

Please answer this question:
{question}
"""
        response = model.generate_content(context)
        st.success("✅ Gemini's Answer:")
        st.write(response.text)

    except Exception as e:
        st.error(f"❌ Error: {e}")
