import os
import pandas as pd
import streamlit as st
import google.generativeai as genai

# 🔐 Gemini API key setup
os.environ["GOOGLE_API_KEY"] = "AIzaSyAEjD-7P2ateq0U0AipxRpy3XgPUKmX6Ww"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Load Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")

st.set_page_config(page_title="Gemini Excel Chatbot", layout="centered")
st.title("📊 Gemini Excel Chatbot")
st.markdown("Ask questions about your uploaded Excel file.")

uploaded_file = st.file_uploader("📁 Upload an Excel file", type=["xlsx"])
question = st.text_input("💬 Ask a question")

# Process and respond
if uploaded_file and question:
    try:
        df = pd.read_excel(uploaded_file)
        st.write("📄 Excel Preview:")
        st.dataframe(df.head(10))

        def dataframe_to_text(df, limit=100):
            return df.head(limit).to_markdown(index=False)

        context = f"""
You are a helpful assistant analyzing data from an Excel file.
Here is a sample of the data:

{dataframe_to_text(df)}

Now, answer the following question based on the full Excel data:
{question}
"""
        response = model.generate_content(context)
        st.success("✅ Gemini Response:")
        st.write(response.text)

    except Exception as e:
        st.error(f"Error: {e}")
