#!/use/bin/python

import os, sys
from io import BytesIO
from pathlib import Path
from flask_config import app
from flask import send_file
from PyPDF2 import PdfFileReader, PdfFileWriter

def rotate_pdf(working_dir, filename, amount):
  os.chdir(working_dir)
  output_name = 'pages'
  rotate_pdf_pages(filename, amount, output_name)
  
  memory_file = BytesIO()
  with open('{}.pdf'.format(output_name), 'rb') as fin:
    memory_file = BytesIO(fin.read())
  memory_file.seek(0)
  os.chdir(os.path.dirname(os.path.realpath(__file__)))
  return send_file(memory_file, attachment_filename='{}.pdf'.format(output_name), as_attachment=True)

def rotate_pdf_pages(filename, amount, output_name):
  pdf_reader = PdfFileReader('{}.pdf'.format(filename))
  pdf_writer = PdfFileWriter()
  
  for page in range(pdf_reader.getNumPages()):
    if amount == '1':
      rotated_page = pdf_reader.getPage(page).rotateClockwise(90)
    if amount == '2':
      rotated_page = pdf_reader.getPage(page).rotateClockwise(180)
    if amount == '3':
      rotated_page = pdf_reader.getPage(page).rotateCounterClockwise(90)
    pdf_writer.addPage(rotated_page)
    
  with open('{}.pdf'.format(output_name), 'wb') as out:
    pdf_writer.write(out)
