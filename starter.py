import speech_recognition as sr
import pyttsx3

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    """Listen from the microphone and convert speech to text."""
    with sr.Microphone() as source:
        print("Listening...")
        # Adjust for ambient noise for better accuracy
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"Recognized: {command}")
        return command.lower()
    except sr.UnknownValueError:
        # When speech is unintelligible
        return ""
    except sr.RequestError:
        # When there is an issue with the speech recognition service
        speak("Sorry, my speech service is down.")
        return ""

def process_command(command):
    """Process the command after the wake word is detected."""
    if "stop" in command:
        speak("Goodbye!")
        exit()
    else:
        # For this example, we'll just echo the command back.
        speak(f"You said: {command}")

def main():
    speak("Jarvis is now running. Say 'Hello Jarvis' to begin.")
    while True:
        # Continuously listen for the wake word
        command = listen()
        if "hello jarvis" in command:
            speak("Hello, how can I help you?")
            # Enter into a loop to process further commands after the wake word
            while True:
                user_command = listen()
                if user_command:
                    # If a stop command is received, break out of the inner loop to re-activate wake word listening.
                    if "stop" in user_command or "goodbye" in user_command:
                        speak("Exiting command mode. Say 'Hello Jarvis' to reactivate.")
                        break
                    else:
                        process_command(user_command)

if __name__ == "__main__":
    main()
