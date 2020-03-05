import os, sys, calendar, time
from pathlib import Path
from flask_config import app
from flask import jsonify
from PyPDF2 import PdfFileReader, PdfFileWriter
from zipfile import ZipFile

def generate_file_name():
  filename = str(calendar.timegm(time.gmtime()))
  Path(app.config['UPLOAD_FOLDER'] + filename).mkdir(parents=True, exist_ok=True)
  return filename + '.pdf'

def split_pdf(filelocation):
  iterate_over_file(filelocation)
  zip_split_files(filelocation)
  resp = jsonify({'message' : 'File successfully uploaded.', 'file location' : filelocation})
  resp.status_code = 201
  return resp

def iterate_over_file(filelocation):
  print(filelocation)
  #os.chdir(filelocation)
  
  filename = filelocation.split('/')[1].split('.')[0]
  
  #zipped_pdfs = ZipFile(filename + '.zip', 'w')
  
  pdf = PdfFileReader(filelocation)
  for page in range(pdf.getNumPages()):
    pdf_writer = PdfFileWriter()
    pdf_writer.addPage(pdf.getPage(page))
    output_filename = 'page_{}.pdf'.format(page + 1)
    
    with open(app.config['UPLOAD_FOLDER'] + filename + '/' + output_filename, 'wb') as out:
      pdf_writer.write(out)
    
    #zipped_pdfs.write(app.config['UPLOAD_FOLDER'] + filename + '/' + output_filename)
  
  #zipped_pdfs.close()
      
def zip_split_files(fileslocation):
  return