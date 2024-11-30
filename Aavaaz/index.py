import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import pyttsx3
from googletrans import Translator
import speech_recognition as sr

# Initialize Translator
translator = Translator()

# Language Options
source_languages = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh-cn",
    "Japanese": "ja",
    "Russian": "ru",
}

target_languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
}

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)  # Adjust noise threshold
        print("Speak something...")

        try:
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

# Translate Text
def translate_text(source_text_box, target_text_box, source_language, target_language):
    source_text = source_text_box.get("1.0", "end-1c")
    src_lang = source_languages[source_language.get()]
    tgt_lang = target_languages[target_language.get()]

    if not source_text.strip():
        CTkMessagebox(title="Input Error", message="Please enter text to translate.")
        return

    try:
        translation = translator.translate(source_text, src=src_lang, dest=tgt_lang)
        target_text_box.delete("1.0", "end")
        target_text_box.insert("1.0", translation.text)
        return translation.text
    except Exception as e:
        CTkMessagebox(title="Translation Error", message=str(e))

# Text-to-Text Translator
def text_to_text():
    translator_window = ctk.CTkToplevel()
    translator_window.title("Text-to-Text Translator")
    translator_window.geometry("500x500")

    ctk.CTkLabel(translator_window, text="Source Language:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    source_language = ctk.CTkComboBox(translator_window, values=list(source_languages.keys()), state="readonly")
    source_language.set("English")
    source_language.grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkLabel(translator_window, text="Target Language:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    target_language = ctk.CTkComboBox(translator_window, values=list(target_languages.keys()), state="readonly")
    target_language.set("English")
    target_language.grid(row=1, column=1, padx=10, pady=10)

    ctk.CTkLabel(translator_window, text="Source Text:").grid(row=2, column=0, padx=10, pady=10, sticky="nw")
    source_text_box = ctk.CTkTextbox(translator_window, height=20, width=140)
    source_text_box.grid(row=2, column=1, padx=10, pady=10)

    ctk.CTkLabel(translator_window, text="Translated Text:").grid(row=3, column=0, padx=10, pady=10, sticky="nw")
    target_text_box = ctk.CTkTextbox(translator_window, height=20, width=140)
    target_text_box.grid(row=3, column=1, padx=10, pady=10)

    translate_button = ctk.CTkButton(
        translator_window,
        text="Translate",
        command=lambda: translate_text(source_text_box, target_text_box, source_language, target_language),
    )
    translate_button.grid(row=4, column=0, columnspan=2, pady=10)

# Speech-to-Speech Translator
def speech_to_speech():
    speech_window = ctk.CTkToplevel()
    speech_window.title("Speech to Speech")
    speech_window.geometry("500x500")

    ctk.CTkLabel(speech_window, text="Source Language:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    source_language = ctk.CTkComboBox(speech_window, values=list(source_languages.keys()), state="readonly")
    source_language.set("English")
    source_language.grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkLabel(speech_window, text="Target Language:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    target_language = ctk.CTkComboBox(speech_window, values=list(target_languages.keys()), state="readonly")
    target_language.set("English")
    target_language.grid(row=1, column=1, padx=10, pady=10)

    ctk.CTkLabel(speech_window, text="Source Text:").grid(row=2, column=0, padx=10, pady=10, sticky="nw")
    source_text_box = ctk.CTkTextbox(speech_window, height=20, width=140)
    source_text_box.grid(row=2, column=1, padx=10, pady=10)

    ctk.CTkLabel(speech_window, text="Translated Text:").grid(row=3, column=0, padx=10, pady=10, sticky="nw")
    target_text_box = ctk.CTkTextbox(speech_window, height=20, width=140)
    target_text_box.grid(row=3, column=1, padx=10, pady=10)

    def handle_translation():
        recognized_text = speech_to_text()
        if recognized_text:
            source_text_box.delete("1.0", "end")
            source_text_box.insert("1.0", recognized_text)
            translated_text = translate_text(source_text_box, target_text_box, source_language, target_language)
            if translated_text:
                engine.say(translated_text)
                engine.runAndWait()

    def clear():
        source_text_box.delete("1.0", "end")
        target_text_box.delete("1.0", "end")

    ctk.CTkButton(speech_window, text="Translate", command=handle_translation).grid(row=4, column=0, columnspan=2, pady=10)
    ctk.CTkButton(speech_window, text="Clear", command=clear).grid(row=5, column=0, columnspan=2, pady=10)

# Main Menu
def main():
    main_window = ctk.CTk()
    main_window.title("Main Menu")
    main_window.geometry("300x200")

    ctk.CTkLabel(main_window, text="Speech Translation App", font=("Arial", 14)).pack(pady=10)
    ctk.CTkButton(main_window, text="Speech to Speech", command=speech_to_speech).pack(pady=5)
    ctk.CTkButton(main_window, text="Text to Text", command=text_to_text).pack(pady=5)

    main_window.mainloop()

# Run the Application
main()
