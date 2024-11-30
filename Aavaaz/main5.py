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
sourced_languages = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh-cn",
    "Japanese": "ja",
    "Russian": "ru",
}

targeted_language={
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
}

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

# Function to translate text
def translate_text(source_text_box, target_text_box, source_language, target_language):
    source_text = source_text_box.get("1.0", "end-1c")
    src_lang = sourced_languages[source_language.get()]
    tgt_lang = targeted_language[target_language.get()]

    if not source_text.strip():
        CTkMessagebox(title = "Input Error", message =  "Please enter text to translate.")
        return

    try:
        translation = translator.translate(source_text, src=src_lang, dest=tgt_lang)
        target_text_box.delete("1.0", "end")
        target_text_box.insert("1.0", translation.text)
        return translation.text
    except Exception as e:
        CTkMessagebox(title = "Translation Error",message =  str(e))

# Function to open the text-to-text translator
def text_to_text():
    translator_window = ctk.CTkToplevel()
    translator_window.title("Text-to-Text Translator")
    translator_window.geometry("500x500")

    l1 = ctk.CTkLabel(translator_window, text="Source Language:")
    l1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    source_language = ctk.CTkComboBox(translator_window, values=list(source_language.keys()), state="readonly")
    source_language.set("Auto Detect")
    source_language.grid(row=0, column=1, padx=10, pady=10)

    l2 = ctk.CTkLabel(translator_window, text="Target Language:")
    l2.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    target_language = ctk.CTkComboBox(translator_window, values=list(target_language.keys()), state="readonly")
    target_language.set("English")
    target_language.grid(row=1, column=1, padx=10, pady=10)

    l3 = ctk.CTkLabel(translator_window, text="Source Text:")
    l3.grid(row=2, column=0, padx=10, pady=10, sticky="nw")
    source_text_box = ctk.CTkTextbox(translator_window, height=20, width=140)
    source_text_box.grid(row=2, column=1, padx=10, pady=10)

    l4 = ctk.CTkLabel(translator_window, text="Translated Text:")
    l4.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
    target_text_box = ctk.CTkTextbox(translator_window, height=20, width=140, state="normal")
    target_text_box.grid(row=3, column=1, padx=10, pady=10)

    translate_button = ctk.CTkButton(
        translator_window,
        text="Translate",
        command=lambda: translate_text(source_text_box, target_text_box, source_language, target_language),
    )
    translate_button.grid(row=4, column=0, columnspan=2, pady=10)
    

engine=pyttsx3.init()

def speech(entry):
    text_to_speak = entry.get()
    if not text_to_speak.strip():
        CTkMessagebox(title="Input Error", message="Please enter text to speak.", icon="warning")
        return
    
    engine.say(text_to_speak)
    engine.runAndWait()
    entry.delete(0,"end")
    
def speech_to_speech():
    speech_window=ctk.CTkToplevel()
    speech_window.title("Speech to Speech")
    speech_window.geometry("500x500")
    
    l1 = ctk.CTkLabel(speech_window, text="Source Language:")
    l1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    source_language = ctk.CTkComboBox(speech_window, values=list(sourced_languages.keys()), state="readonly")
    source_language.set("English")
    source_language.grid(row=0, column=1, padx=10, pady=10)

    l2 = ctk.CTkLabel(speech_window, text="Target Language:")
    l2.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    target_language = ctk.CTkComboBox(speech_window, values=list(targeted_language.keys()), state="readonly")
    target_language.set("English")
    
    target_language.grid(row=1, column=1, padx=10, pady=10)
    l3 = ctk.CTkLabel(speech_window, text="Source Text:")
    l3.grid(row=2, column=0, padx=10, pady=10, sticky="nw")
    source_text_box = ctk.CTkTextbox(speech_window, height=20, width=140)
    source_text_box.grid(row=2, column=1, padx=10, pady=10)

    l4 = ctk.CTkLabel(speech_window, text="Translated Text:")
    l4.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
    target_text_box = ctk.CTkTextbox(speech_window, height=20, width=140, state="normal")
    target_text_box.grid(row=3, column=1, padx=10, pady=10)
    
    def clear():
        source_text_box.delete("1.0","end")
        target_text_box.delete("1.0","end")

    def handle_translation():
        recognized_text = speech_to_text()  # Call the speech_to_text function
        if recognized_text:
            # Populate source_text_box
            source_text_box.delete("1.0", "end")
            source_text_box.insert("1.0", recognized_text)

            # Translate the recognized text
            translated_text=translate_text(source_text_box, target_text_box, source_language, target_language)
            engine.say(translated_text)
            engine.runAndWait()
        
 
    translate_button = ctk.CTkButton(
        speech_window,
        text="Translate",
        command=handle_translation,  # Use the wrapper function
    )
    translate_button.grid(row=4, column=0, columnspan=2, pady=10)
    
    clear_button=ctk.CTkButton(speech_window,text='Clear',command=clear)
    clear_button.grid(row=5,column=0,columnspan=2,pady=10)

    


# Function to open the text-to-speech translator
def text_to_speech():
    volume = engine.getProperty('volume')
    print(volume)  # Printing current volume level
    engine.setProperty('volume', 1)  # Setting volume level between 0 and 1

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Female voice

    rate = engine.getProperty('rate')
    print(rate)  # Printing current voice rate
    engine.setProperty('rate', 125)  # Setting up new voice rate

    tts_window = ctk.CTkToplevel()
    tts_window.title("Text-to-Speech Translator")
    tts_window.geometry("500x500")

    l1 = ctk.CTkLabel(tts_window, text="Source Language:")
    l1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    source_languaged = ctk.CTkComboBox(tts_window, values=list(sourced_languages.keys()), state="readonly")
    source_languaged.set("Auto Detect")
    source_languaged.grid(row=0, column=1, padx=10, pady=10)

    l2 = ctk.CTkLabel(tts_window, text="Target Language:")
    l2.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    target_languaged = ctk.CTkComboBox(tts_window, values=list(targeted_language.keys()), state="readonly")
    target_languaged.set("English")
    target_languaged.grid(row=1, column=1, padx=10, pady=10)

    l3 = ctk.CTkLabel(tts_window, text="Source Text:")
    l3.grid(row=2, column=0, padx=10, pady=10, sticky="nw")
    source_text_box = ctk.CTkEntry(tts_window, height=20, width=140)
    source_text_box.grid(row=2, column=1, padx=10, pady=10)

    l4 = ctk.CTkLabel(tts_window, text="Translated Text:")
    l4.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
    target_text_box = ctk.CTkEntry(tts_window, height=20, width=140, state="normal")
    target_text_box.grid(row=3, column=1, padx=10, pady=10)

    # Function to handle translation and speaking of translated text
    def translate_and_speak():
        source_text = source_text_box.get()
        src_lang = sourced_languages[source_languaged.get()]
        tgt_lang = targeted_language[target_languaged.get()]

        if not source_text.strip():
            CTkMessagebox(title="Input Error", message="Please enter text to translate.", icon="warning")
            return

        try:
            # Translate text
            translation = translator.translate(source_text, src=src_lang, dest=tgt_lang)
            translated_text = translation.text

            # Display translated text
            target_text_box.delete("1.0", "end")
            target_text_box.insert("1.0", translated_text)

            # Speak the translated text
            engine.say(translated_text)
            engine.runAndWait()

        except Exception as e:
            CTkMessagebox(title="Translation Error", message=f"Error: {str(e)}", icon="error")

    # Translate & Speak Button
    translate_button = ctk.CTkButton(
        tts_window,
        text="Translate & Speak",
        command=translate_and_speak
    )
    translate_button.grid(row=4, column=0, columnspan=2, pady=10)


# Main Menu
def main():
    main_window = ctk.CTk()
    main_window.title("Main Menu")
    main_window.geometry("300x200")

    ctk.CTkLabel(main_window, text="Speech Translation App", font=("Arial", 14)).pack(pady=10)

    ctk.CTkButton(main_window, text="Speech to Speech", command=speech_to_speech).pack(pady=5)
    ctk.CTkButton(main_window, text="Speech to Text", command=lambda: messagebox.showinfo("Feature", "Coming Soon!")).pack(pady=5)
    ctk.CTkButton(main_window, text="Text to Speech", command=text_to_speech).pack(pady=5)
    ctk.CTkButton(main_window, text="Text to Text", command=text_to_text).pack(pady=5)

    main_window.mainloop()

# Run the Main Menu
main()