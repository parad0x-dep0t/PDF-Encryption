import logging 
from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter

def get_pdf_reader(input_path):
  return PdfReader(input_path.open("rb"))

def write_protected_pdf(pdf_writer, output_path):
  with output_path.open("wb") as output_file:
    pdf_writer.write(output_file)

def add_password_protection(pdf_reader, password):
  pdf_writer = PdfWriter()
  for page in pdf_reader.pages:
    pdf_writer.add_page(page)
  pdf_writer.encrypt(password)
  return pdf_writer

def protect_pdf(input_path, output_path, password):
  input_path = Path(input_path)
  if not input_path.exists():
    print(f"Input file not found: {input_path}")
    return

  pdf_reader = get_pdf_reader(input_path)
  pdf_writer = add_password_protection(pdf_reader, password)
  write_protected_pdf(pdf_writer, output_path)

  print("PDF protected successfully.")

if __name__ == "__main__":

  input_pdf = input("Enter path to input PDF: ")
  output_pdf = Path(f"protected_{input_pdf}") 
  password = "your_password"

  protect_pdf(input_pdf, output_pdf, password)