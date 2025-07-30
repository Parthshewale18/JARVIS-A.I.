from http.client import responses
import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import datetime
import random
import google.generativeai as genai
from env import GEMINI_API_KEY
#---------------------------------------------------------------------------------------
def say(text):
    engine = pyttsx3.init()
    #rate=engine.getProperty('rate') #Default = 200
    engine.setProperty('rate', 150)#Slower speech
    #setting volume
    #volume = engine.getProperty('volume')  # default is 1.0
    engine.setProperty('volume', 0.8)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)# 0 for male & 1 for female.
    engine.say(text)
    engine.runAndWait()
#---------------------------------------------------------------------------------------
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #r.pause_threshold = 1 ByDefault it set to 0.8
        audio = r.listen(source)
        try:
           print("Recognizing...")
           query = r.recognize_google(audio,language='en-in')
           print(f"PARTH:{query}")

           return query
        except Exception as e:
            return "Sorry, didn't recognize your input."

#---------------------------------------------------------------------------------------

API_KEY = GEMINI_API_KEY

def chat_with_gemini(user_input):
    # Configure the API
    genai.configure(api_key=API_KEY)

    # Use the chat-compatible model
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")

    # Start a conversation
    chat = model.start_chat()

    try:
        response = chat.send_message(user_input)
        reply = response.text.strip()

        print("JARVIS:", reply)
        print()

        # Speak the output
        engine = pyttsx3.init()
        engine.say(reply)
        engine.runAndWait()

        return reply
    except Exception as e:
        print("Error:", e)
        return "Something went wrong."

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
if __name__=="__main__":
    say("Hello, I am JARVIS A.I.")
    while True:
      print("Listening...")
      query = takeCommand()
      #say(query)
      sites = [['youtube','https://www.youtube.com'],['google','https://www.google.com']]
      apps = [['VS code',r"C:\Users\Admin\AppData\Local\Programs\Microsoft VS Code\Code.exe"],['Docker',r"C:\Program Files\Docker\Docker\Docker Desktop.exe"]]
      if "open".lower() in query.lower():
          for site in sites:
              if f"Open {site[0]}".lower() in query.lower():
                  say(f"openning {site[0]} sir...")
                  webbrowser.open(site[1])
          for app in apps:
              if f"open {app[0]}".lower() in query.lower():
                  path=app[1]
                  say(f"openning {app[0]} sir...")
                  os.startfile(path)
      elif "play music" in query:
          music_path="C:\\Users\\Admin\\Music\\music\\i_guess_krsna.mp3"
          os.startfile(music_path)
          exit()
      elif "the time".lower() in query.lower():
          hour = datetime.datetime.now().strftime("%H")
          min = datetime.datetime.now().strftime("%M")
          say(f"sir the time is {hour}:{min} ")
      elif "who made you".lower() in query.lower():
          say("The great Paarth made me.")
      elif "Jarvis sleep".lower() in query.lower():
          say("ok, I am now going to sleep, wakeup me, when you need my help, Bye Bye!")
          exit()
      elif "shutdown".lower() in query.lower():
          say("Shuting down the pc")
          os.system("shutdown /s /t 1")
      else:
          response=chat_with_gemini(query)
