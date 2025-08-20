import streamlit as st
import os, webbrowser, datetime
import google.generativeai as genai
import pyttsx3
from env import GEMINI_API_KEY

# ------------------- Speech Output -------------------
def say(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.8)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id) # male voice
    engine.say(text)
    engine.runAndWait()

# ------------------- Gemini Chat -------------------
API_KEY = GEMINI_API_KEY
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")
chat = model.start_chat()

def chat_with_gemini(user_input):
    try:
        response = chat.send_message(user_input)
        reply = response.text.strip()
        return reply
    except Exception as e:
        return f"Error: {e}"

# ------------------- Streamlit UI -------------------
st.set_page_config(page_title="Jarvis AI", page_icon="🤖", layout="centered")
st.title("🤖 Jarvis AI Assistant")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello, I am Jarvis. How can I help you today?"}
    ]

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ------------------- Handle commands -------------------
    sites = {'youtube': 'https://www.youtube.com', 'google': 'https://www.google.com'}
    apps = {
        'vs code': r"C:\Users\Admin\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        'docker': r"C:\Program Files\Docker\Docker\Docker Desktop.exe"
    }

    response = None

    if "open" in prompt.lower():
        for name, link in sites.items():
            if f"open {name}" in prompt.lower():
                response = f"Opening {name}..."
                webbrowser.open(link)
        for name, path in apps.items():
            if f"open {name}" in prompt.lower():
                response = f"Opening {name}..."
                os.startfile(path)
    elif "play music" in prompt.lower():
        music_path = "C:\\Users\\Admin\\Music\\music\\i_guess_krsna.mp3"
        os.startfile(music_path)
        response = "Playing your music 🎵"
    elif "time" in prompt.lower():
        now = datetime.datetime.now().strftime("%H:%M")
        response = f"The time is {now}"
    elif "who made you" in prompt.lower():
        response = "The great Paarth made me"
    elif "shutdown" in prompt.lower():
        response = "Shutting down the PC..."
        os.system("shutdown /s /t 1")
    elif "sleep" in prompt.lower():
        response = "Okay, Jarvis going to sleep. Bye!"
    else:
        response = chat_with_gemini(prompt)

    # Add assistant response
    st.session_state["messages"].append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

    # Optional: Voice output
    say(response)
