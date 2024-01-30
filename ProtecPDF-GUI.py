import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import fitz  # PyMuPDF
from PyPDF2 import PdfReader, PdfWriter

# PDF protector functions

def extract_links(input_path):
    input_path = Path(input_path)
    links = []
    
    pdf_reader = fitz.open(input_path)
    
    for page_number in range(pdf_reader.page_count):
        page = pdf_reader[page_number]
        links.extend(page.get_links())
    
    pdf_reader.close()
    return links

def add_links_to_pdf(pdf_writer, links):
    for link in links:
        rect_info = link.get('rect', [])
        if len(rect_info) == 4:
            rect = fitz.Rect(rect_info)
            uri = link.get('uri', '')
            from_page = link.get('from', 0)
            to_page = link.get('to', 0)
            pdf_writer.addLink(uri, rect, int(from_page), int(to_page))

def protect_pdf(input_path, output_path, password):
    input_path = Path(input_path)
    if not input_path.exists():
        return False

    links = extract_links(input_path)

    pdf_reader = PdfReader(input_path.open("rb"))
    pdf_writer = PdfWriter()

    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]
        pdf_writer.add_page(page)

    with open(output_path, "wb") as output_file:  # Explicitly create a Path object for output_path
        pdf_writer.encrypt(password)
        add_links_to_pdf(pdf_writer, links)
        pdf_writer.write(output_file)

    return True

def decrypt_pdf(input_path, output_path, password):
    input_path = Path(input_path)
    if not input_path.exists():
        return False

    pdf_reader = PdfReader(input_path.open("rb"))
    pdf_writer = PdfWriter()

    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]
        pdf_writer.add_page(page)

    with open(output_path, "wb") as output_file:  # Explicitly create a Path object for output_path
        pdf_writer.decrypt(password)
        pdf_writer.write(output_file)

    return True

# GUI code

root = tk.Tk()
root.title("PDF Protector")

# Input PDF path
pdf_path = tk.StringVar()

def browse_file():
    filename = filedialog.askopenfilename()
    pdf_path.set(filename)

browse_btn = tk.Button(root, text="Browse", command=browse_file)
browse_btn.grid(row=0, column=2)

pdf_entry = tk.Entry(root, textvariable=pdf_path)
pdf_entry.grid(row=0, column=1)

# Password input
password = tk.StringVar()

tk.Label(root, text="Password").grid(row=1, column=0)
password_entry = tk.Entry(root, show="*", textvariable=password)
password_entry.grid(row=1, column=1)

# Protect PDF button
def protect():
    input_path = pdf_path.get()
    pwd = password.get()
    protected = protect_pdf(input_path, "protected.pdf", pwd)

    if protected:
        result_label.config(text="Protected successfully!")
    else:
        result_label.config(text="Error protecting PDF")

protect_btn = tk.Button(root, text="Protect PDF", command=protect)
protect_btn.grid(row=2, column=0, columnspan=2)

# Decrypt PDF button
def decrypt():
    input_path = pdf_path.get()
    pwd = password.get()
    decrypted = decrypt_pdf(input_path, "decrypted.pdf", pwd)

    if decrypted:
        result_label.config(text="Decrypted successfully!")
    else:
        result_label.config(text="Error decrypting PDF")

decrypt_btn = tk.Button(root, text="Decrypt PDF", command=decrypt)
decrypt_btn.grid(row=3, column=0, columnspan=2)

# Result label
result_label = tk.Label(root)
result_label.grid(row=4, column=0, columnspan=2)

root.mainloop()
