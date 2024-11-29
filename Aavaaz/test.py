import customtkinter as ctk
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from tkinter import messagebox as tkmsg
import threading

# Initialize the translator and languages
translator = Translator()
languages = LANGUAGES  # Dictionary of language codes and their full names

# Function to translate speech to text and open translated window
def speechToText(src_lang_name, tgt_lang_name):
    # Hide the main window
    translator_window.withdraw()

    # Create a new Speak Window for speech recognition
    speak_window = ctk.CTkToplevel()
    speak_window.title("Speak Window")
    speak_window.geometry("300x200")

    # Add labels to show the process
    l1 = ctk.CTkLabel(speak_window, text="Adjusting for background noise... Please wait.")
    l1.grid(row=0, column=0, padx=10, pady=10)

    l2 = ctk.CTkLabel(speak_window, text="Say something!")
    l2.grid(row=1, column=0, padx=10, pady=10)

    # Call the speech recognition process in a separate thread
    threading.Thread(target=lambda: process_speech(speak_window, src_lang_name, tgt_lang_name)).start()

# Function to process speech input and show translation
def process_speech(speak_window, src_lang_name, tgt_lang_name):
    recognizer = sr.Recognizer()

    # Mapping languages to their codes
    src_lang = languages.get(src_lang_name, "auto")
    tgt_lang = languages.get(tgt_lang_name, "en")

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        # Recognize the speech
        source_text = recognizer.recognize_google(audio, language=src_lang)

        # Translate the speech to the target language
        translation = translator.translate(source_text, src=src_lang, dest=tgt_lang)

        # Open translated text window and show result
        show_translated_window(translation.text)

    except Exception as e:
        tkmsg.showerror("Error", f"Error: {e}")
    finally:
        # Close the Speak Window
        speak_window.destroy()

# Function to show translated text in a new window
def show_translated_window(translated_text):
    # Create a new Toplevel window for translation
    translated_window = ctk.CTkToplevel()
    translated_window.title("Translated Text")
    translated_window.geometry("500x300")

    # Label to display translated text
    translated_label = ctk.CTkLabel(translated_window, text="Translated Text:")
    translated_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    target_text_box = ctk.CTkTextbox(translated_window, height=150, width=300)
    target_text_box.grid(row=1, column=0, padx=10, pady=10)
    target_text_box.insert("1.0", translated_text)

    # Button to close the translated window and show the main window again
    close_button = ctk.CTkButton(translated_window, text="Close", command=lambda: close_translated_window(translated_window))
    close_button.grid(row=2, column=0, pady=10)

# Function to close the translated window and show the main window again
def close_translated_window(translated_window):
    translated_window.destroy()
    translator_window.deiconify()  # Show the main window again

# Main GUI Setup
translator_window = ctk.CTk()
translator_window.title("Speech-to-Text Translator")
translator_window.geometry("500x600")

# Label and ComboBox for selecting source language
source_language_label = ctk.CTkLabel(translator_window, text="Source Language:")
source_language_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

source_language = ctk.CTkComboBox(translator_window, values=list(languages.keys()), state="readonly")
source_language.set("Auto Detect")
source_language.grid(row=0, column=1, padx=10, pady=10)

# Label and ComboBox for selecting target language
target_language_label = ctk.CTkLabel(translator_window, text="Target Language:")
target_language_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

target_language = ctk.CTkComboBox(translator_window, values=list(languages.keys()), state="readonly")
target_language.set("English")
target_language.grid(row=1, column=1, padx=10, pady=10)

# Button to open speech-to-text window
speak_button = ctk.CTkButton(
    translator_window,
    text="Speak Here",
    command=lambda: speechToText(source_language.get(), target_language.get())
)
speak_button.grid(row=2, column=0, columnspan=2, pady=10)

# Run the GUI
translator_window.mainloop()
