#!/use/bin/python

import os, sys
from io import BytesIO, StringIO
from pathlib import Path
from flask_config import app
from flask import send_file
from PyPDF2 import PdfFileReader, PdfFileWriter
from zipfile import ZipFile, ZIP_DEFLATED

def split_pdf(pdffile, filename):
  pdf = PdfFileReader(pdffile)
  pages = []
  
  for page in range(pdf.getNumPages()):
    pages.append(('page_{}.pdf'.format(page + 1), get_page_from_pdf(page, pdffile)))
    
  memory_file = add_files_to_zip(pages)
  memory_file.seek(0)
  return send_file(memory_file, attachment_filename='{}.zip'.format(filename), as_attachment=True)

def get_page_from_pdf(pagenr, pdffile):
  page_as_bytesio = BytesIO()
  pdf_writer = PdfFileWriter()
  pdf_writer.addPage(PdfFileReader(pdffile).getPage(pagenr))
  
  pdf_writer.write(page_as_bytesio)
  page_as_bytesio.seek(0)
  return page_as_bytesio

def add_files_to_zip(files):
  mem_zip = BytesIO()
  zipped_pdfs = ZipFile(mem_zip, 'a', ZIP_DEFLATED)
  
  for f in files:
    zipped_pdfs.writestr(f[0], f[1].getbuffer())
    
  zipped_pdfs.close()
  return mem_zip
