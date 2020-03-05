import os, sys, calendar, time, datetime, base64
from io import BytesIO
from pathlib import Path
from flask_config import app
from flask import send_file
from PyPDF2 import PdfFileReader, PdfFileWriter
from zipfile import ZipFile

def generate_file_name():
  filename = str(calendar.timegm(time.gmtime()))
  return str(filename)

def create_dir(filename):
  currentYear = str(datetime.datetime.now().year)
  currentMonth = str(datetime.datetime.now().month)
  currentDay = str(datetime.datetime.now().day)
  new_dir = os.path.join(app.config['UPLOAD_FOLDER'], currentYear, currentMonth, currentDay, filename)
  Path(new_dir).mkdir(parents=True, exist_ok=True)
  return new_dir

def split_pdf(working_dir, filename):
  iterate_over_file(working_dir, filename)
  memory_file = BytesIO()
  with open('{}.zip'.format(filename), 'rb') as fin:
    memory_file = BytesIO(fin.read())
  memory_file.seek(0)
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