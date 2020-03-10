#!/use/bin/python

import os, sys
from io import BytesIO
from pathlib import Path
from flask_config import app
from flask import send_file
from PyPDF2 import PdfFileReader, PdfFileWriter
from zipfile import ZipFile

def split_pdf(working_dir, filename):
  iterate_over_file(working_dir, filename)
  memory_file = BytesIO()
  with open('{}.zip'.format(filename), 'rb') as fin:
    memory_file = BytesIO(fin.read())
  memory_file.seek(0)
  os.chdir(os.path.dirname(os.path.realpath(__file__)))
  return send_file(memory_file, attachment_filename='{}.zip'.format(filename), as_attachment=True)

def iterate_over_file(working_dir, filename):
  os.chdir(working_dir)
  
  zipped_pdfs = ZipFile('{}.zip'.format(filename), 'w')
  pdf = PdfFileReader('{}.pdf'.format(filename))
  
  for page in range(pdf.getNumPages()):
    pdf_writer = PdfFileWriter()
    pdf_writer.addPage(pdf.getPage(page))
    output_filename = 'page_{}.pdf'.format(page + 1)
    
    with open(output_filename, 'wb') as out:
      pdf_writer.write(out)
    
    zipped_pdfs.write(output_filename)
  
  zipped_pdfs.close()