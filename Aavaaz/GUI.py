import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from googletrans import Translator
import speech_recognition as sr

# Initialize Translator
translator = Translator()

# Language Options
languages = {
    "Auto Detect": "auto",
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh-cn",
    "Japanese": "ja",
    "Russian": "ru",
}


# Function to open the speech-to-text translator
def speechToTextGUI():
    translator_window = ctk.CTkToplevel()
    translator_window.title("Speech-to-Text Translator")
    translator_window.geometry("500x600")

    #translated_text = ctk.StringVar(value="")

    #Function to translate speech to text
    def speechToText(src_lang, tgt_lang):
        speak_window = ctk.CTkToplevel()
        speak_window.title("Speak Window")

        # Initialize recognizer
        recognizer = sr.Recognizer()


        # Use microphone as source
        with sr.Microphone() as source:
            l1 = ctk.CTkLabel(speak_window, text="Adjusting for background noise... Please wait.")
            l1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            recognizer.adjust_for_ambient_noise(source)  # Reduce noise
            l2 = ctk.CTkLabel(speak_window, text="Say something!")
            l2.grid(row=0, column=1, padx=10, pady=10, sticky="w")
            audio = recognizer.listen(source)  # Capture audio

        try:
            # Recognize speech using Google's Web Speech API
            print("You said: " + recognizer.recognize_google(audio))
            source_text = recognizer.recognize_google(audio)
            translation = translator.translate(source_text, src=src_lang, dest=tgt_lang)
            t = translation.text
            target_text_box.delete("1.0", "end")
            target_text_box.insert("1.0", t)
            speak_window.destroy()
        except sr.UnknownValueError:
            CTkMessagebox(title = "Error", message =  "Sorry, I could not understand the audio.")
            speak_window.destroy()
        except sr.RequestError as e:
            CTkMessagebox(title = "Error", message =  f"Could not request results from Google Speech Recognition service; {e}")
            speak_window.destroy()

    l1 = ctk.CTkLabel(translator_window, text="Source Language:")
    l1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    source_language = ctk.CTkComboBox(translator_window, values=list(languages.keys()), state="readonly")
    source_language.set("Auto Detect")
    source_language.grid(row=0, column=1, padx=10, pady=10)

    l2 = ctk.CTkLabel(translator_window, text="Target Language:")
    l2.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    target_language = ctk.CTkComboBox(translator_window, values=list(languages.keys()), state="readonly")
    target_language.set("English")
    target_language.grid(row=1, column=1, padx=10, pady=10)

    # l3 = ctk.CTkLabel(translator_window, text="Source Text:")
    # l3.grid(row=2, column=0, padx=10, pady=10, sticky="nw")
    # source_text_box = ctk.CTkTextbox(translator_window, height=200, width=300)
    # source_text_box.grid(row=2, column=1, padx=10, pady=10)

    speak_button = ctk.CTkButton(
        translator_window,
        text="Speak Here",
        command=lambda: speechToText(source_language, target_language),
    )
    speak_button.grid(row=3, column=1, padx=10, pady=10)

    l4 = ctk.CTkLabel(translator_window, text="Translated Text:")
    l4.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
    target_text_box = ctk.CTkTextbox(translator_window, height=200, width=300, state="normal")
    target_text_box.grid(row=4, column=1, padx=10, pady=10)

    # translate_button = ctk.CTkButton(
    #     translator_window,
    #     text="Translate",
    #     command=lambda: translate_text(source_text_box, target_text_box, source_language, target_language),
    # )
    #translate_button.grid(row=4, column=0, columnspan=2, pady=10)
    translator_window.mainloop()



# Function to translate text
def translate_text(source_text_box, target_text_box, source_language, target_language):
    source_text = source_text_box.get("1.0", "end-1c")
    src_lang = languages[source_language.get()]
    tgt_lang = languages[target_language.get()]

    if not source_text.strip():
        CTkMessagebox(title = "Input Error", message =  "Please enter text to translate.")
        return

    try:
        translation = translator.translate(source_text, src=src_lang, dest=tgt_lang)
        target_text_box.delete("1.0", "end")
        target_text_box.insert("1.0", translation.text)
    except Exception as e:
        CTkMessagebox(title = "Translation Error",message =  str(e))


def text_to_text():
    translator_window = ctk.CTkToplevel()
    translator_window.title("Text-to-Text Translator")
    translator_window.geometry("500x600")

    l1 = ctk.CTkLabel(translator_window, text="Source Language:")
    l1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    source_language = ctk.CTkComboBox(translator_window, values=list(languages.keys()), state="readonly")
    source_language.set("Auto Detect")
    source_language.grid(row=0, column=1, padx=10, pady=10)

    l2 = ctk.CTkLabel(translator_window, text="Target Language:")
    l2.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    target_language = ctk.CTkComboBox(translator_window, values=list(languages.keys()), state="readonly")
    target_language.set("English")
    target_language.grid(row=1, column=1, padx=10, pady=10)

    l3 = ctk.CTkLabel(translator_window, text="Source Text:")
    l3.grid(row=2, column=0, padx=10, pady=10, sticky="nw")
    source_text_box = ctk.CTkTextbox(translator_window, height=200, width=300)
    source_text_box.grid(row=2, column=1, padx=10, pady=10)

    l4 = ctk.CTkLabel(translator_window, text="Translated Text:")
    l4.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
    target_text_box = ctk.CTkTextbox(translator_window, height=200, width=300, state="normal")
    target_text_box.grid(row=3, column=1, padx=10, pady=10)

    translate_button = ctk.CTkButton(
        translator_window,
        text="Translate",
        command=lambda: translate_text(source_text_box, target_text_box, source_language, target_language),
    )
    translate_button.grid(row=4, column=0, columnspan=2, pady=10)
    translator_window.mainloop()


# Main Menu
def main():
    main_window = ctk.CTk()
    main_window.title("Main Menu")
    main_window.geometry("300x200")

    ctk.CTkLabel(main_window, text="Speech Translation App", font=("Arial", 14)).pack(pady=10)

    ctk.CTkButton(main_window, text="Speech to Speech", command=lambda: messagebox.showinfo("Feature", "Coming Soon!")).pack(pady=5)
    ctk.CTkButton(main_window, text="Speech to Text", command=speechToTextGUI).pack(pady=5)
    ctk.CTkButton(main_window, text="Text to Speech", command=lambda: messagebox.showinfo("Feature", "Coming Soon!")).pack(pady=5)
    ctk.CTkButton(main_window, text="Text to Text", command=text_to_text).pack(pady=5)

    main_window.mainloop()

# Run the Main Menu
main()
