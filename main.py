from http.client import responses

import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import datetime
import openai
import random
import google.generativeai as genai
from env import OPENAI_API_KEY

# todo this in future:
# def ai(prompt):
#     openai.api_key = OPENAI_API_KEY
#     # prompt = "Write an email to my boss for resignation?"
#     test = f"Openai response for prompt : {prompt}\n **************\n\n"
#     # response = openai.Completion.create(
#     #     model="text-davinci-003",
#     #     prompt=prompt,
#     #     temperature=0.8,
#     #     max_tokens=256,
#     #     top_p=0.9,
#     #     frequency_penalty=0.0,
#     #     presence_penalty=0.0
#     # )
#     #----------------------------------------------
#     client = openai.OpenAI(api_key=OPENAI_API_KEY)
#
#     response = client.completions.create(
#         model="text-davinci-003",
#         prompt="Your prompt here",
#         max_tokens=100,
#         temperature=0.7
#     )
#
#     print(response.choices[0].text.strip())
#     #------------------------------------------
#     print(response["choices"][0]["text"])
#     text += response["choices"][0]["text"]
#     if not os.path.exists("Openai"):
#         os.mkdir("Openai")
#     with open(f"prompt-{random.randint(1,12343434356)}.txt", "w") as f:
#         f.write(response["choices"][0]["text"])
#---------------------------------------------------------------------------------------
def say(text):
    engine = pyttsx3.init()
    #rate=engine.getProperty('rate') #Default = 200
    engine.setProperty('rate', 150)#Slower speech
    #setting volume
    volume = engine.getProperty('volume')  # default is 1.0
    engine.setProperty('volume', 0.4)
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
           print(f"User said:{query}")
           return query
        except Exception as e:
            return "Sorry, didn't recognize your input."

#---------------------------------------------------------------------------------------

API_KEY = OPENAI_API_KEY

def chat_with_gemini(user_input):
    # Configure the API
    genai.configure(api_key=API_KEY)

    # Use the chat-compatible model
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")

    # Start a conversation
    chat = model.start_chat()

    try:
        response = chat.send_message(user_input)
        reply = response.text.strip()

        print("Jarvis:", reply)

        # Speak the output
        engine = pyttsx3.init()
        engine.say(reply)
        engine.runAndWait()

        return reply
    except Exception as e:
        print("Error:", e)
        return "Something went wrong."

#---------------------------------------------------------------------------------------
# openai.api_key = OPENAI_API_KEY
# def chat_with_gpt(prompt):
#     response = openai.chat.completions.create(
#         model = "gpt-3.5-turbo",
#         messages=[{'role':'user', 'content':prompt}],
#     )
#     return response.choices[0].message.content.strip()
#---------------------------------------------------------------------------------------
if __name__=="__main__":
    say("Hello, I am JARVIS A.I.")
    while True:
      print("Listening...")
      query = takeCommand()
      #say(query)
      sites = [['youtube','https://www.youtube.com'],['google','https://www.google.com']]
      apps = [['VS code',r"C:\Users\Admin\AppData\Local\Programs\Microsoft VS Code\Code.exe"],['Docker',r"C:\Program Files\Docker\Docker\Docker Desktop.exe"]]
      for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            say(f"openning {site[0]} sir...")
            webbrowser.open(site[1])
      if "Play music" in query:
          music_path=""
          os.startfile(music_path)
      for app in apps:
          if f"open {app[0]}".lower() in query.lower():
             path=app[1]
             say(f"openning {app[0]} sir...")
             os.startfile(path)
      if "the time".lower() in query.lower():
          hour = datetime.datetime.now().strftime("%H")
          min = datetime.datetime.now().strftime("%M")
          say(f"sir the time is {hour}:{min} ")
       #todo:
      # if "Using AI".lower() in query.lower():
      #     ai(prompt=query)
      if "Jarvis sleep".lower() in query.lower():
          exit()
      elif "shutdown".lower() in query.lower():
          os.system("shutdown /s /t 1")
      else:
          response=chat_with_gemini(query)
          print("JARVIS :", response)