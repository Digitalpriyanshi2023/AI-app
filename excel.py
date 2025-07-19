import os
import pandas as pd
import google.generativeai as genai

# ⛅ Replace with your actual Gemini API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyAEjD-7P2ateq0U0AipxRpy3XgPUKmX6Ww"

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# 🧠 Setup Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")

# 📖 Load Excel file dynamically each time
def load_excel(file_path="computer.xlsx"):
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print("❌ Error reading Excel:", e)
        return None

# 📄 Convert DataFrame to markdown format
def dataframe_to_text(df, limit=100):
    try:
        return df.head(limit).to_markdown(index=False)
    except Exception as e:
        return f"Error converting dataframe: {e}"

# 💬 Ask question to Gemini with Excel data
def chat_with_excel(question, file_path="computer.xlsx"):
    df = load_excel(file_path)
    if df is None:
        return "Sorry, couldn't load the Excel data."
    
    context = f"""
You are a helpful assistant analyzing employee salary data from an Excel file.
Here is a sample of the data:

{dataframe_to_text(df)}

Now, answer the following question based on the full Excel data:
{question}
"""
    try:
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"❌ Gemini API Error: {e}"

# ▶️ Main Loop
def main():
    print("📊 Gemini Excel Chatbot is ready! Ask questions (type 'exit' to quit):\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Bot: Goodbye!")
            break
        answer = chat_with_excel(user_input)
        print("Bot:", answer, "\n")

if __name__ == "__main__":
    main()
