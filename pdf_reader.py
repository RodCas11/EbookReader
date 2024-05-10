import PyPDF2
import re

class PDFReader:
    def __init__(self):
        self.pdf_file = None
        self.pdf_reader = None
        self.file_handle = None  # Handle to the open PDF file

    def open_pdf(self, file_path):
        if self.file_handle:  # Se já houver um arquivo aberto, feche-o
            self.file_handle.close()
        self.pdf_file = file_path
        self.file_handle = open(self.pdf_file, 'rb')
        self.pdf_reader = PyPDF2.PdfFileReader(self.file_handle)

    def read_page(self, page_num):
        if self.pdf_reader is None or page_num >= self.pdf_reader.numPages:
            raise Exception("Page number out of range or PDF not loaded")
        page = self.pdf_reader.getPage(page_num)
        text = page.extractText()
        return self.adjust_text(text)

    def get_page_count(self):
        if self.pdf_reader is None:
            raise Exception("No PDF file loaded")
        return self.pdf_reader.numPages

    def adjust_text(self, text):
        text = re.sub(r'-\s*\n', '', text)  # Remove hyphens at line breaks
        text = re.sub(r'\n', ' ', text)  # Replace new lines with spaces
        return text

    def close_pdf(self):
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None