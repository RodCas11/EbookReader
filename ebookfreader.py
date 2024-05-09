import PyPDF2
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import time
import pickle
import os

class PDFReader:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Reader")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Helvetica', 12))

        self.text = tk.Label(self.root, wraplength=600, font=("Helvetica", 14))
        self.text.pack(fill="both", expand=True)

        file_button = ttk.Button(self.root, text="Selecionar PDF", command=self.select_pdf)
        file_button.pack(side="top", pady=10)

        speed_frame = tk.Frame(self.root)
        speed_frame.pack(side="top", pady=10)

        self.speed_label = tk.Label(speed_frame, text="Velocidade:", font=("Helvetica", 12))
        self.speed_label.pack(side="left", padx=10)

        self.speed_var = tk.StringVar()
        self.speed_var.set("500")
        self.speed_menu = ttk.OptionMenu(speed_frame, self.speed_var, "200", "300", "500", "600", "1000")
        self.speed_menu.pack(side="left", padx=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack(side="bottom", pady=10)

        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_reading)
        self.start_button.pack(side="left", padx=10)

        self.resume_button = ttk.Button(button_frame, text="Resume", command=self.resume_reading)
        self.resume_button.pack(side="left", padx=10)

        self.pause_button = ttk.Button(button_frame, text="Pause", command=self.pause_reading)
        self.pause_button.pack(side="left", padx=10)

        self.page_label = tk.Label(self.root, text="Página: 1", font=("Helvetica", 12))
        self.page_label.pack(side="bottom", pady=10)

        self.current_pdf_state = {}
        self.pdf_file = None
        self.is_reading = False
        self.load_state()

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
            pdf_reader = PyPDF2.PdfFileReader(open(self.pdf_file, "rb"))
            current_page, current_word = self.current_pdf_state[self.pdf_file]
            while current_page < pdf_reader.numPages and self.is_reading:
                page = pdf_reader.getPage(current_page)
                text = page.extractText()
                words = text.split()
                start_index = words.index(current_word) + 1 if current_word in words else 0
                for word in words[start_index:]:
                    if not self.is_reading:
                        break
                    self.text.config(text=word)
                    self.root.update()
                    time.sleep(60 / float(self.speed_var.get()))
                    current_word = word
                if not self.is_reading:
                    break
                current_page += 1
                current_word = ""
                self.page_label.config(text=f"Página: {current_page + 1}")
                self.current_pdf_state[self.pdf_file] = (current_page, current_word)
                if current_page >= pdf_reader.numPages:
                    break

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