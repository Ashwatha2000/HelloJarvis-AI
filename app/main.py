import json
import openai
import requests
import pyaudio
import pyttsx3
from vosk import Model, KaldiRecognizer

# ✅ Load API key from config.json
with open("./config/config.json", "r") as config_file:
    config = json.load(config_file)
    openai.api_key = config["openai_api_key"]

# Initialize the TTS engine
tts_engine = pyttsx3.init()

def speak(text):
    """Convert AI response to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

# Load Vosk Speech Model
model_path = "models/vosk-model-en-us-0.22-lgraph"
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# Set up PyAudio
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=16000,
                 input=True,
                 frames_per_buffer=8000)
stream.start_stream()

print("Listening for 'hello jarvis'...")

while True:
    data = stream.read(4000, exception_on_overflow=False)
    
    if len(data) == 0:
        break

    if recognizer.AcceptWaveform(data):
        result_json = json.loads(recognizer.Result())
        text = result_json.get("text", "").lower()
        print("Recognized:", text)

        # Check for wake word
        if "hello jarvis" in text:
            print("Wake word detected!")
            speak("Hello, Developer. How can I help you?")
            
            # 🛑 Instead of stopping, now continue listening for a user question
            print("Listening for your question...")

            while True:
                data = stream.read(4000, exception_on_overflow=False)
                if recognizer.AcceptWaveform(data):
                    result_json = json.loads(recognizer.Result())
                    user_query = result_json.get("text", "").strip()
                    
                    if user_query:
                        print(f"User asked: {user_query}")
                        break  # Exit loop when query is received
            
            # Send user query to OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Or "gpt-4" for better responses
                messages=[{"role": "system", "content": "You are a helpful assistant."},
                          {"role": "user", "content": user_query}]
            )

            ai_text = response["choices"][0]["message"]["content"]
            print(f"AI Response: {ai_text}")
            speak(ai_text)
