import json
import pyaudio
from vosk import Model, KaldiRecognizer
import pyttsx3

# Initialize the TTS engine
tts_engine = pyttsx3.init()

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Path to your Vosk model directory (adjust as needed)
model_path = "models/vosk-model-en-us-0.22-lgraph"
# Initialize the Vosk model
model = Model(model_path)
# Create a recognizer for 16kHz audio
recognizer = KaldiRecognizer(model, 16000)

# Set up PyAudio to capture audio from the microphone
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
    # Check if we have enough data
    if len(data) == 0:
        break
    if recognizer.AcceptWaveform(data):
        result_json = json.loads(recognizer.Result())
        text = result_json.get("text", "").lower()
        print("Recognized:", text)
        # Check for the exact keyphrase
        if "hello jarvis" in text:
            print("Wake word detected!")
            speak("Hello, Developer. How can I help you?")
            break
    else:
        # Optionally, you can print partial results for debugging:
        partial = json.loads(recognizer.PartialResult()).get("partial", "")
        # Uncomment the next line to see partial recognition output:
        # print("Partial:", partial)

stream.stop_stream()
stream.close()
pa.terminate()
