import os, sys, calendar, time
from pathlib import Path
from flask_config import app
from flask import jsonify
from PyPDF2 import PdfFileReader, PdfFileWriter

def generate_file_name():
  filename = str(calendar.timegm(time.gmtime()))
  Path(app.config['UPLOAD_FOLDER'] + filename).mkdir(parents=True, exist_ok=True)
  return filename + '.pdf'

def split_pdf(filelocation):
  iterate_over_file(filelocation)
  resp = jsonify({'message' : 'File successfully uploaded.', 'file location' : filelocation})
  resp.status_code = 201
  return resp

def iterate_over_file(filelocation):
  filename = filelocation.split('/')[1].split('.')[0]
  print(filename)
  pdf = PdfFileReader(filelocation)
  for page in range(pdf.getNumPages()):
    pdf_writer = PdfFileWriter()
    pdf_writer.addPage(pdf.getPage(page))
    output_filename = 'page_{}.pdf'.format(page + 1)
    
    with open(app.config['UPLOAD_FOLDER'] + filename + '/' + output_filename, 'wb') as out:
      pdf_writer.write(out)