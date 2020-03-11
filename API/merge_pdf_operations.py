#!/use/bin/python

import os, sys
from io import BytesIO
from pathlib import Path
from flask_config import app
from flask import send_file
from PyPDF2 import PdfFileMerger
from zipfile import ZipFile

def merge_pdf(working_dir, filename):
  os.chdir(working_dir)
  extract_zip(filename)
  merge_pdf_pages()
  
  memory_file = BytesIO()
  with open('{}.pdf'.format('pages'), 'rb') as fin:
    memory_file = BytesIO(fin.read())
  memory_file.seek(0)
  os.chdir(os.path.dirname(os.path.realpath(__file__)))
  return send_file(memory_file, attachment_filename='{}.pdf'.format('pages'), as_attachment=True)

def extract_zip(filename):
  with ZipFile('{}.zip'.format(filename), 'r') as zipObj:
    list_of_file_names = zipObj.namelist()
    for file_name_in_zip in list_of_file_names:
        if file_name_in_zip.endswith('.pdf'):
            zipObj.extract(file_name_in_zip)

def merge_pdf_pages():
  pdf_merger = PdfFileMerger()
  files = [f for f in os.listdir('.') if os.path.isfile(f)]
  files.sort()
  for f in files:
    if ('.pdf' in f):
      pdf_merger.append(f)
  with open('pages.pdf', 'wb') as out:
    pdf_merger.write(out)
