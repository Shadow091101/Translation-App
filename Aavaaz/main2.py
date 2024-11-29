import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator

# Initialize Translator
translator = Translator()

# Function to translate text
def translate_text():
    source_text = source_text_box.get("1.0", "end-1c")
    source_lang = source_language.get()
    target_lang = target_language.get()

    if not source_text.strip():
        messagebox.showwarning("Input Error", "Please enter text to translate.")
        return

    try:
        translation = translator.translate(source_text, src=source_lang, dest=target_lang)
        target_text_box.delete("1.0", "end")
        target_text_box.insert("1.0", translation.text)
    except Exception as e:
        messagebox.showerror("Translation Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("Language Translator")
root.geometry("500x400")

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



# Widgets
tk.Label(root, text="Source Language:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
source_language = ttk.Combobox(root, values=list(languages.keys()), state="readonly")
source_language.set("Auto Detect")
source_language.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Target Language:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
target_language = ttk.Combobox(root, values=list(languages.keys()), state="readonly")
target_language.set("English")
target_language.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Source Text:").grid(row=2, column=0, padx=10, pady=10, sticky="nw")
source_text_box = tk.Text(root, height=8, width=40)
source_text_box.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Translated Text:").grid(row=3, column=0, padx=10, pady=10, sticky="nw")
target_text_box = tk.Text(root, height=8, width=40, state="normal")
target_text_box.grid(row=3, column=1, padx=10, pady=10)

translate_button = tk.Button(root, text="Translate", command=translate_text, bg="blue", fg="white")
translate_button.grid(row=4, column=0, columnspan=2, pady=10)

# Run the Application
root.mainloop()