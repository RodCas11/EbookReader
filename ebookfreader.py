import PyPDF2
import tkinter as tk
from tkinter import filedialog
import time

class PDFReader:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Reader")
        self.text = tk.Label(self.root, wraplength=500, font=("Helvetica", 14))
        self.text.pack(fill="both", expand=True)

        file_button = tk.Button(self.root, text="Selecionar PDF", command=self.select_pdf)
        file_button.pack(side="top", pady=10)

        speed_frame = tk.Frame(self.root)
        speed_frame.pack(side="top", pady=10)

        self.speed_label = tk.Label(speed_frame, text="Speed:")
        self.speed_label.pack(side="left", padx=10)

        self.speed_var = tk.StringVar()
        self.speed_var.set("500")
        self.speed_menu = tk.OptionMenu(speed_frame, self.speed_var, "200", "300", "500", "600", "1000")
        self.speed_menu.pack(side="left", padx=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack(side="bottom", pady=10)

        self.start_button = tk.Button(button_frame, text="Start", command=self.start_reading)
        self.start_button.pack(side="left", padx=10)
        
        self.resume_button = tk.Button(button_frame, text="Resume", command=self.resume_reading)
        self.resume_button.pack(side="left", padx=10)
        
        self.pause_button = tk.Button(button_frame, text="Pause", command=self.pause_reading)
        self.pause_button.pack(side="left", padx=10)

        self.current_speed = 500
        self.is_reading = False
        self.word_history = []

        self.page_label = tk.Label(self.root, text="Página: 1")
        self.page_label.pack(side="bottom", pady=10)

        self.page_number = 1  # Inicializa o número da página
        self.last_word = None
        self.last_page = 1

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Lidar com o fechamento do aplicativo

    def select_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.pdf_file = file_path
            self.load_pdf()

    def load_pdf(self):
        with open(self.pdf_file, "rb") as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            num_pages = pdf_reader.numPages
            text = ""
            self.page_first_word_index = [0]  # Armazena o índice da primeira palavra de cada página
            for page_num in range(num_pages):
                if self.page_number > page_num + 1:
                    continue
                page = pdf_reader.getPage(page_num)
                text += page.extractText()
                self.page_first_word_index.append(len(text.split()))  # Adiciona o índice da primeira palavra da próxima página
            self.words = text.split()

    def start_reading(self):
        if not self.is_reading and hasattr(self, 'pdf_file'):
            self.is_reading = True
            self.current_speed = int(self.speed_var.get())
            self.load_state()
            if self.last_word:
                try:
                    word_index = self.words.index(self.last_word)
                    self.words = self.words[word_index:]
                except ValueError:
                    self.last_word = None
                    self.last_page = 1
            self.read_words()

    def pause_reading(self):
        self.is_reading = False
        if self.word_history:
            self.last_word = self.word_history[-1]  # Armazenar a última palavra
            self.last_page = self.find_current_page()  # Determinar a página correspondente
            self.save_state()

    def resume_reading(self):
        if not self.is_reading:
            self.is_reading = True
            self.read_words()

    def read_words(self):
        if self.is_reading:
            for index, word in enumerate(self.words):
                self.text.config(text=word)
                self.root.update()
                self.word_history.append(word)
                time.sleep(60 / self.current_speed)
                if not self.is_reading:
                    break
                if index in self.page_first_word_index:
                    self.page_number += 1  # Incrementa o número da página
                    self.page_label.config(text=f"Página: {self.page_number}")  # Atualiza a label da página

    def save_state(self):
        with open("reader_state.txt", "w") as file:
            file.write(f"{self.last_word}\n{self.last_page}")

    def load_state(self):
        try:
            with open("reader_state.txt", "r") as file:
                lines = file.read().strip().split("\n")
                if len(lines) == 2:
                    self.last_word, self.last_page = lines
                    self.last_page = int(self.last_page)
        except FileNotFoundError:
            pass

    def find_current_page(self):
        for index, first_word_index in enumerate(self.page_first_word_index):
            if first_word_index <= len(self.word_history):
                return index + 1  # O índice da página começa em 1
        return 1

    def on_close(self):
        self.save_state()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    pdf_reader = PDFReader()
    pdf_reader.run()