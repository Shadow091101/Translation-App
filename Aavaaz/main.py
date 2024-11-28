import speech_recognition as sr
from googletrans import Translator
import pyttsx3

# Initialize translator and TTS engine
translator = Translator()
engine = pyttsx3.init()

# Function: Convert speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)  # Adjust noise threshold
        print("Speak something...")

        try:
            # Listen until silence for at least 5 seconds
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
            text = recognizer.recognize_google(audio)
            print(f"Recognized Speech: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"API error: {e}")
            return None

# Function: Translate text
def translate_text(text, target_lang="hi"):
    translated = translator.translate(text, dest=target_lang)
    print(f"Translated Text: {translated.text}")
    return translated.text

# Function: Convert text to speech
def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

# Main function start the code from here
def speech_to_speech(target_lang="hi"):
    # Step 1: Capture Speech
    original_text = speech_to_text()
    if original_text is None:
        return

    # Step 2: Translate Speech
    translated_text = translate_text(original_text, target_lang)

    # Step 3: Speak the Translated Speech
    print("Speaking Translated Speech...")
    text_to_speech(translated_text)

# Run the speech-to-speech translator
if __name__ == "__main__":
    target_language = "hi"  # Change to desired language code (e.g., "fr" for French, "de" for German)
    speech_to_speech(target_lang=target_language)
