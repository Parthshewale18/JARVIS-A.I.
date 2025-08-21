import streamlit as st
import datetime
import google.generativeai as genai

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# ------------------- Gemini Chat Setup -------------------
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

    # Command handling with cloud-safe alternatives
    sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com"
    }

    response = None
    lower_prompt = prompt.lower()

    if "open" in lower_prompt:
        for name, link in sites.items():
            if f"open {name}" in lower_prompt:
                response = f"[Opening {name}]({link})"
                break
        if response is None:
            response = "Sorry, I can't open that site."
    elif "play music" in lower_prompt:
        response = "Playing music is not supported in this cloud app."
    elif "time" in lower_prompt:
        now = datetime.datetime.now().strftime("%H:%M")
        response = f"The time is {now}"
    elif "who made you" in lower_prompt:
        response = "The great Parth made me"
    elif "shutdown" in lower_prompt:
        response = "Shutting down PC is not supported here."
    elif "sleep" in lower_prompt:
        response = "Okay, Jarvis going to sleep. Bye!"
    else:
        response = chat_with_gemini(prompt)

    # Add assistant response
    st.session_state["messages"].append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
