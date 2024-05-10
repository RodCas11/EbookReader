import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pdf_reader import PDFReader
from config import themes

class PDFReaderUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Reader")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.pdf_reader = PDFReader()
        self.current_page = 0
        self.current_char_index = 0
        self.current_page_content = ""
        self.is_reading = False
        self.current_theme = "Light"  # Definir antes de setup_ui()
        self.setup_ui()

    def setup_ui(self):
        control_frame = tk.Frame(self.root, bg=themes[self.current_theme]["highlight"])
        control_frame.pack(side="top", fill="x", pady=5)

        file_button = ttk.Button(control_frame, text="Selecionar PDF", command=self.select_pdf)
        file_button.pack(side="left", padx=10)

        self.start_button = ttk.Button(control_frame, text="Start", command=self.start_reading)
        self.start_button.pack(side="left")

        self.resume_button = ttk.Button(control_frame, text="Resume", command=self.resume_reading)
        self.resume_button.pack(side="left")

        self.pause_button = ttk.Button(control_frame, text="Pause", command=self.pause_reading)
        self.pause_button.pack(side="left")

        settings_frame = tk.Frame(self.root, bg=themes[self.current_theme]["highlight"])
        settings_frame.pack(side="top", fill="x", pady=5)

        tk.Label(settings_frame, text="Tema:", bg=themes[self.current_theme]["highlight"]).pack(side="left", padx=10)
        theme_menu = ttk.Combobox(settings_frame, values=list(themes.keys()), state="readonly", width=10)
        theme_menu.set(self.current_theme)
        theme_menu.pack(side="left")
        theme_menu.bind("<<ComboboxSelected>>", self.change_theme)

        tk.Label(settings_frame, text="Velocidade:", bg=themes[self.current_theme]["highlight"]).pack(side="left", padx=10)
        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_scale = ttk.Scale(settings_frame, from_=0.5, to=3.0, orient='horizontal', variable=self.speed_var, length=200)
        self.speed_scale.pack(side="left")

        self.text = tk.Label(self.root, font=("Helvetica", 14), wraplength=600)
        self.text.pack(fill="both", expand=True, padx=10, pady=10)

        self.page_label = tk.Label(self.root, font=("Helvetica", 12))
        self.page_label.pack(side="bottom", pady=5)

        self.apply_theme(self.current_theme)

    def change_theme(self, event):
        new_theme = event.widget.get()
        self.apply_theme(new_theme)

    def apply_theme(self, theme):
        self.root.configure(background=themes[theme]["background"])
        self.text.configure(background=themes[theme]["background"], foreground=themes[theme]["foreground"])
        self.page_label.configure(background=themes[theme]["background"], foreground=themes[theme]["foreground"])
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(background=themes[theme]["background"])

    def on_close(self):
        self.pdf_reader.close_pdf()
        self.root.destroy()

    def select_pdf(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.pdf_reader.close_pdf()  # Fechar o arquivo atual antes de abrir um novo
            self.pdf_reader.open_pdf(file_path)
            self.current_page = 0
            self.current_page_content = ""
            self.page_label.config(text="Página: 1")
            self.text.config(text="")

    def start_reading(self):
        self.is_reading = True
        self.read_pdf()

    def read_pdf(self):
        if self.current_page_content == "" or self.current_char_index >= len(self.current_page_content):
        # Se o conteúdo da página atual acabou ou ainda não foi carregado, carregue a próxima página
            if self.current_page >= self.pdf_reader.get_page_count():
                messagebox.showinfo("Fim", "Você chegou ao final do documento.")
                self.is_reading = False
            return
        
        try:
            self.current_page_content = self.pdf_reader.read_page(self.current_page)
            self.current_char_index = 0
            self.current_page += 1
            self.page_label.config(text=f"Página: {self.current_page}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            self.is_reading = False
            return

    # Continua a exibir o texto letra por letra
        if self.is_reading and self.current_char_index < len(self.current_page_content):
            next_char = self.current_page_content[self.current_char_index]
            self.current_char_index += 1
            current_text = self.text['text'] + next_char
            self.text.config(text=current_text)

        # Agendar a próxima atualização
            delay = int(1000 / (20 * self.speed_var.get()))  # Ajustar a velocidade de exibição
            self.root.after(delay, self.read_pdf)
        else:
        # Reset quando chegar ao fim da página para começar uma nova página
            self.current_page_content = ""
            self.read_pdf()

    def pause_reading(self):
        self.is_reading = False

    def resume_reading(self):
        if not self.is_reading:
            self.is_reading = True
            self.read_pdf()

    def run(self):
        self.root.mainloop()