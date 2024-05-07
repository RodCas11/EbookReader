import PyPDF2
import tkinter as tk
from tkinter import filedialog
import time

class PDFReader:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Reader")
        self.root.configure(bg='#333')  # Dark background color

        self.text = tk.Label(self.root, wraplength=500, font=("Helvetica", 14), bg='#333', fg='white')  # Dark background with white text
        self.text.pack(fill="both", expand=True)

        file_button = tk.Button(self.root, text="Select PDF", command=self.select_pdf)
        file_button.pack(side="top", pady=10)

        speed_frame = tk.Frame(self.root, bg='#333')  # Dark background color
        speed_frame.pack(side="top", pady=10)

        self.speed_label = tk.Label(speed_frame, text="Speed:", bg='#333', fg='white')  # Dark background with white text
        self.speed_label.pack(side="left", padx=10)

        self.speed_var = tk.StringVar()
        self.speed_var.set("500")
        self.speed_menu = tk.OptionMenu(speed_frame, self.speed_var, "200", "300", "500", "600", "1000")
        self.speed_menu.pack(side="left", padx=10)

        button_frame = tk.Frame(self.root, bg='#333')  # Dark background color
        button_frame.pack(side="bottom", pady=10)

        self.start_button = tk.Button(button_frame, text="Start", command=self.start_reading)
        self.start_button.pack(side="left", padx=10)
        
        self.pause_button = tk.Button(button_frame, text="Pause", command=self.pause_reading)
        self.pause_button.pack(side="left", padx=10)

        self.save_button = tk.Button(button_frame, text="Save Page Number", command=self.save_page_number)
        self.save_button.pack(side="left", padx=10)

        self.load_button = tk.Button(button_frame, text="Load Page Number", command=self.load_page_number)
        self.load_button.pack(side="left", padx=10)

        self.current_speed = 500
        self.is_reading = False
        self.current_page = 0
        self.conf_file = None

    def select_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.pdf_file = file_path
            self.load_pdf()
            self.conf_file = self.pdf_file + ".conf"
            self.load_page_number()

    def load_pdf(self):
        with open(self.pdf_file, "rb") as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            self.num_pages = pdf_reader.numPages
            text = ""
            for page_num in range(self.num_pages):
                page = pdf_reader.getPage(page_num)
                text += page.extractText()
            self.words = text.split()

    def start_reading(self):
        if not self.is_reading and hasattr(self, 'pdf_file'):
            self.is_reading = True
            self.current_speed = int(self.speed_var.get())
            self.read_words()

    def pause_reading(self):
        self.is_reading = False

    def save_page_number(self):
        with open(self.conf_file, "w") as conf_file:
            conf_file.write(str(self.current_page))

    def load_page_number(self):
        try:
            with open(self.conf_file, "r") as conf_file:
                self.current_page = int(conf_file.read())
                if self.current_page >= self.num_pages:
                    self.current_page = 0
        except FileNotFoundError:
            self.current_page = 0

    def read_words(self):
        if self.is_reading:
            for page_num in range(self.current_page, self.num_pages):
                page = self.words[page_num]
                self.text.config(text=page)
                self.current_page = page_num
                self.root.update()
                time.sleep(60 / self.current_speed)  # Adjust the speed here
                if not self.is_reading:
                    break

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    pdf_reader = PDFReader()
    pdf_reader.run()