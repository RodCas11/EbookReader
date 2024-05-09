import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import time
import pickle
import os
import re

class PDFReader:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Reader")
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.themes = {
            "Light": {"background": "white", "foreground": "black", "highlight": "#D6D6D6"},
            "Dark": {"background": "#363636", "foreground": "white", "highlight": "#5C5C5C"},
            "Blue": {"background": "#282c34", "foreground": "#abb2bf", "highlight": "#5C5C5C"}
        }
        self.current_theme = "Light"

        # Layout configuration
        control_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]["highlight"])
        control_frame.pack(side="top", fill="x", pady=5)

        file_button = ttk.Button(control_frame, text="Selecionar PDF", command=self.select_pdf)
        file_button.pack(side="left", padx=10)

        self.start_button = ttk.Button(control_frame, text="Start", command=self.start_reading)
        self.start_button.pack(side="left")

        self.resume_button = ttk.Button(control_frame, text="Resume", command=self.resume_reading)
        self.resume_button.pack(side="left")

        self.pause_button = ttk.Button(control_frame, text="Pause", command=self.pause_reading)
        self.pause_button.pack(side="left")

        settings_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]["highlight"])
        settings_frame.pack(side="top", fill="x", pady=5)

        tk.Label(settings_frame, text="Tema:", bg=self.themes[self.current_theme]["highlight"]).pack(side="left", padx=10)
        theme_menu = ttk.Combobox(settings_frame, values=list(self.themes.keys()), state="readonly", width=10)
        theme_menu.set(self.current_theme)
        theme_menu.pack(side="left")
        theme_menu.bind("<<ComboboxSelected>>", self.change_theme)

        tk.Label(settings_frame, text="Velocidade:", bg=self.themes[self.current_theme]["highlight"]).pack(side="left", padx=10)
        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_scale = ttk.Scale(settings_frame, from_=0.5, to=3.0, orient='horizontal', variable=self.speed_var, length=200)
        self.speed_scale.pack(side="left")

        self.text = tk.Label(self.root, font=("Helvetica", 14), wraplength=600)
        self.text.pack(fill="both", expand=True, padx=10, pady=10)

        self.page_label = tk.Label(self.root, font=("Helvetica", 12))
        self.page_label.pack(side="bottom", pady=5)

        self.apply_theme(self.current_theme)
        self.current_pdf_state = {}
        self.pdf_file = None
        self.is_reading = False
        self.load_state()

    def change_theme(self, event):
        self.current_theme = event.widget.get()
        self.apply_theme(self.current_theme)

    def apply_theme(self, theme):
        self.root.configure(background=self.themes[theme]["background"])
        self.text.configure(background=self.themes[theme]["background"], foreground=self.themes[theme]["foreground"])
        self.page_label.configure(background=self.themes[theme]["background"], foreground=self.themes[theme]["foreground"])
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(background=self.themes[theme]["background"])

    def select_pdf(self):
        new_pdf_file = filedialog.askopenfilename()
        if new_pdf_file and new_pdf_file != self.pdf_file:
            self.pdf_file = new_pdf_file
            self.root.title(f"PDF Reader - {os.path.basename(self.pdf_file)}")
            self.current_pdf_state[self.pdf_file] = self.current_pdf_state.get(self.pdf_file, (0, ""))
            self.load_pdf_state()
            self.read_pdf()

    def start_reading(self):
        self.is_reading = True
        self.read_pdf()

    def read_pdf(self):
        if self.pdf_file and self.is_reading:
            try:
                pdf_reader = PyPDF2.PdfFileReader(open(self.pdf_file, "rb"))
                current_page, current_word = self.current_pdf_state[self.pdf_file]
                while current_page < pdf_reader.numPages and self.is_reading:
                    page = pdf_reader.getPage(current_page)
                    raw_text = page.extractText()
                    text = self.adjust_text(raw_text)
                    words = text.split()
                    start_index = words.index(current_word) + 1 if current_word in words else 0
                    for word in words[start_index:]:
                        if not self.is_reading:
                            break
                        self.text.config(text=word)
                        self.root.update()
                        time.sleep(60 / (500 * self.speed_var.get()))
                        current_word = word
                    current_page += 1
                    current_word = ""
                    self.page_label.config(text=f"Página: {current_page + 1}")
                    self.current_pdf_state[self.pdf_file] = (current_page, current_word)
                    if current_page >= pdf_reader.numPages:
                        break
            except Exception as e:
                messagebox.showerror("Error", "Cannot open PDF: " + str(e))

    def adjust_text(self, text):
        # Remove inappropriate hyphens and new lines
        text = re.sub(r'-\s*\n', '', text)
        text = re.sub(r'\n', ' ', text)
        return text

    def pause_reading(self):
        self.is_reading = False
        self.save_state()

    def resume_reading(self):
        if self.pdf_file in self.current_pdf_state:
            self.is_reading = True
            self.read_pdf()

    def save_state(self):
        with open("reader_state.pickle", "wb") as file:
            pickle.dump(self.current_pdf_state, file)

    def load_state(self):
        try:
            with open("reader_state.pickle", "rb") as file:
                self.current_pdf_state = pickle.load(file)
        except FileNotFoundError:
            self.current_pdf_state = {}

    def load_pdf_state(self):
        if self.pdf_file in self.current_pdf_state:
            page, word = self.current_pdf_state[self.pdf_file]
            self.page_label.config(text=f"Página: {page + 1}")

    def on_close(self):
        self.pause_reading()
        self.root.destroy()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

if __name__ == "__main__":
    pdf_reader = PDFReader()
    pdf_reader.run()