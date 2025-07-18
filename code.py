import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import google.generativeai as genai

# Configure your API key here
API_KEY = "AIzaSyAEjD-7P2ateq0U0AipxRpy3XgPUKmX6Ww"
MODEL_NAME = "models/gemini-1.5-flash"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)
chat = model.start_chat()


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Chat App - Priyanshi")
        self.root.geometry("600x600")
        self.root.configure(bg="#f0f0f0")

        # Chat display area (scrollable)
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled',
                                                      font=("Segoe UI", 12), bg="#ffffff")
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Input frame
        input_frame = tk.Frame(root, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        self.user_input = tk.Entry(input_frame, font=("Segoe UI", 12))
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.user_input.bind("<Return>", self.send_message)

        send_button = tk.Button(input_frame, text="Send", command=self.send_message,
                                bg="#4CAF50", fg="white", font=("Segoe UI", 12, "bold"),
                                activebackground="#45a049", padx=15, pady=5)
        send_button.pack(side=tk.RIGHT)

        self.append_chat("AI", "Hello! Ask me anything. Type 'bye' to exit.")

    def append_chat(self, sender, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)  # Scroll to bottom

    def send_message(self, event=None):
        user_text = self.user_input.get().strip()
        if not user_text:
            return

        self.append_chat("You", user_text)
        self.user_input.delete(0, tk.END)

        if user_text.lower() in ["exit", "quit", "bye"]:
            self.append_chat("AI", "Bye Priyanshi! 👋")
            self.root.after(1000, self.root.destroy)
            return

        # Run API call in a thread to avoid freezing the UI
        threading.Thread(target=self.get_ai_response, args=(user_text,), daemon=True).start()

    def get_ai_response(self, user_text):
        try:
            response = chat.send_message(user_text)
            self.append_chat("AI", response.text)
        except Exception as e:
            self.append_chat("AI", f"❌ Error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
