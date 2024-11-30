import threading
import pyttsx3
import time
import speech_recognition as sr
from googletrans import Translator

engine = pyttsx3.init()

def text_to_speech_async(text="Hello, this is a test of the text-to-speech function."):

    def speak():
        engine.say(text)
        engine.runAndWait()
        print("Finished Speaking ....")

    # Run in a separate thread to avoid blocking
    t = threading.Thread(target=speak)
    t.start()
    
    # Join the thread to ensure the main thread waits for the speaking to finish
    t.join()

# Test the asynchronous function
text_to_speech_async("Hello, this is a test of the text-to-speech function.")
