import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from googletrans import Translator
import speech_recognition as sr
import threading


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
    translator_window.geometry("500x400+500+100")
    translator_window.grab_set()

    translated_text = ctk.StringVar(value="")

    # Function to translate speech to text
    def speechToText(src_lang_name, tgt_lang_name):
        # Create the Speak Window
        speak_window = ctk.CTkToplevel(translator_window)
        speak_window.title("Speak Window")
        speak_window.geometry("300x200")
        speak_window.grab_set()

        # Add labels to show the process
        l1 = ctk.CTkLabel(speak_window, text="Adjusting for background noise... Please wait.")
        l1.grid(row=0, column=0, padx=10, pady=10)

        l2 = ctk.CTkLabel(speak_window, text="Say something!")
        l2.grid(row=1, column=0, padx=10, pady=10)

        def process_speech(speak_window, src_lang_name, tgt_lang_name):
            recognizer = sr.Recognizer()

            # Language mapping
            src_lang = languages.get(src_lang_name, "auto")
            tgt_lang = languages.get(tgt_lang_name, "en")

            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)

                # Recognize and translate
                source_text = recognizer.recognize_google(audio, language=src_lang)
                translation = translator.translate(source_text, src=src_lang, dest=tgt_lang)

                # Update the translated text box
                target_text_box.delete("1.0", "end")
                target_text_box.insert("1.0", translation.text)
            except Exception as e:
                CTkMessagebox(title="Error", message=f"Error: {e}")
            finally:
                # Ensure the Speak Window is destroyed
                speak_window.destroy()

        # Call the rest of the function in a thread to avoid blocking the UI
        threading.Thread(target=lambda: process_speech(speak_window, src_lang_name, tgt_lang_name)).start()


    # def speechToText(src_lang_name, tgt_lang_name):
    #     speak_window = ctk.CTkToplevel()
    #     speak_window.title("Speak Window")

    #     recognizer = sr.Recognizer()

    #     # Validate language codes
    #     src_lang = languages.get(src_lang_name, "auto")  # Default to auto-detect
    #     tgt_lang = languages.get(tgt_lang_name, "en")   # Default to English

    #     if not src_lang or not tgt_lang:
    #         CTkMessagebox(title="Error", message="Invalid language selection.")
    #         speak_window.destroy()
    #         return

    #     # Use the microphone as source
    #     with sr.Microphone() as source:
    #         ctk.CTkLabel(speak_window, text="Adjusting for background noise... Please wait.").grid(
    #             row=0, column=0, padx=10, pady=10
    #         )
    #         recognizer.adjust_for_ambient_noise(source)
    #         ctk.CTkLabel(speak_window, text="Say something!").grid(
    #             row=1, column=0, padx=10, pady=10
    #         )
    #         audio = recognizer.listen(source)

    #     try:
    #         # Recognize speech
    #         source_text = recognizer.recognize_google(audio, language=src_lang)

    #         # Translate text
    #         translation = translator.translate(source_text, src=src_lang, dest=tgt_lang)

    #         # Insert translation into the CTkTextbox
    #         target_text_box.delete("1.0", "end")
    #         target_text_box.insert("1.0", translation.text)
    #     except sr.UnknownValueError:
    #         CTkMessagebox(title="Error", message="Sorry, I could not understand the audio.")
    #     except sr.RequestError as e:
    #         CTkMessagebox(title="Error", message=f"Request failed: {e}")
    #     except Exception as e:
    #         CTkMessagebox(title="Error", message=f"An error occurred: {e}")
    #     finally:
    #         # Close the speak window
    #         speak_window.destroy()


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

    speak_button = ctk.CTkButton(
    translator_window,
    text="Speak Here",
    command=lambda: speechToText(source_language.get(), target_language.get())
    )
    speak_button.grid(row=2, column=0, columnspan=2, pady=10)

    l4 = ctk.CTkLabel(translator_window, text="Translated Text:")
    l4.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
    target_text_box = ctk.CTkTextbox(translator_window, height=200, width=300)
    target_text_box.grid(row=3, column=1, padx=10, pady=10)

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
    main_window.geometry("300x210+100+100")

    ctk.CTkLabel(main_window, text="Speech Translation App", font=("Arial", 14)).pack(pady=10)

    ctk.CTkButton(main_window, text="Speech to Speech", command=lambda: messagebox.showinfo("Feature", "Coming Soon!")).pack(pady=5)
    ctk.CTkButton(main_window, text="Speech to Text", command=speechToTextGUI).pack(pady=5)
    ctk.CTkButton(main_window, text="Text to Speech", command=lambda: messagebox.showinfo("Feature", "Coming Soon!")).pack(pady=5)
    ctk.CTkButton(main_window, text="Text to Text", command=text_to_text).pack(pady=5)

    main_window.mainloop()

# Run the Main Menu
main()
