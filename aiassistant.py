import pyttsx3
import  speech_recognition as sr
import os
from dotenv import load_dotenv

import google.generativeai as genai

engine = pyttsx3.init()
r = sr.Recognizer()
mic = sr.Microphone(device_index=0)

conversation = ""
user_name = input("Enter your name: ")

rate = engine.getProperty('rate')
engine.setProperty('rate', 225)

voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)  # changing index, changes voices. 0 for male
engine.setProperty('voice', voices[1].id)  # changing index, changes voices. 1 for female

load_dotenv()

API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

while True:
    with mic as source:
        print("\nAI: Listening... speak clearly into mic.")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    print("No longer listening.\n")

    try:
        user_input = r.recognize_google(audio)
    except:
        continue

    prompt = user_name + ": " + user_input
    conversation += prompt

    response = chat.send_message(conversation, stream=True)
    response.resolve()
    response_str = response.text

    conversation += response_str + "\n"
    print("AI: " + response.text)

    engine.say(response.text)
    engine.runAndWait()

    if "Goodbye" in response.text:
        break

engine.stop()
# print("AI: Goodbye, have a nice day!")



