#!/use/bin/python

import os, sys
from io import BytesIO
from pathlib import Path
from flask_config import app
from flask import send_file
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from zipfile import ZipFile

def get_pages_pdf(working_dir, filename, pages, returntype):
  os.chdir(working_dir)
  extract_pages(filename, pages)
  
  if (returntype == 'pdf'):
    merge_pdf_pages()

  if (returntype == 'zip'):
    zip_pdf_pages()
  
  memory_file = BytesIO()
  with open('pages.{}'.format(returntype), 'rb') as fin:
    memory_file = BytesIO(fin.read())
  memory_file.seek(0)
  os.chdir(os.path.dirname(os.path.realpath(__file__)))
  return send_file(memory_file, attachment_filename='pages.{}'.format(returntype), as_attachment=True)

def extract_pages(filename, pages):
  pdf = PdfFileReader('{}.pdf'.format(filename))
  for page in range(pdf.getNumPages()):
    if (page + 1 in pages):
      pdf_writer = PdfFileWriter()
      pdf_writer.addPage(pdf.getPage(page))
      output_filename = 'page_{}.pdf'.format(page + 1)
      with open(output_filename, 'wb') as out:
        pdf_writer.write(out)

def merge_pdf_pages():
  pdf_merger = PdfFileMerger()
  files = [f for f in os.listdir('.') if os.path.isfile(f)]
  for f in files:
    if ('page_' in f):
      pdf_merger.append(f)
  with open('pages.pdf', 'wb') as out:
        pdf_merger.write(out)

def zip_pdf_pages():
  zipped_pdfs = ZipFile('pages.zip', 'w')
  files = [f for f in os.listdir('.') if os.path.isfile(f)]
  files.sort()
  for f in files:
    if ('page_' in f):
      zipped_pdfs.write(f)
      
  zipped_pdfs.close()
