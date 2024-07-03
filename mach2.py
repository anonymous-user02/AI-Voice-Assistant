import speech_recognition as sr
import os
from dotenv import load_dotenv
from gtts import gTTS
from IPython.display import Audio
import google.generativeai as genai
import tempfile
import playsound 

    
r = sr.Recognizer()
mic = sr.Microphone(device_index=0)

conversation = ""
user_name = input("Enter your name: ")

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
    
    print(conversation)

    response = chat.send_message(conversation, stream=True)
    response.resolve()
    response_str = response.text

    conversation += response_str + "\n"
    print("AI: " + response.text)

   

    # Using gTTS for text to speech
    tts = gTTS(text=response.text, lang='hi')
    # Save the audio file
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts.save(fp.name + '.mp3')
        # Play the audio file
        playsound.playsound(fp.name + '.mp3')

    if "Goodbye" in response.text:
        break

