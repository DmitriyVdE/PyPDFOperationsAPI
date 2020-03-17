#!/use/bin/python

import os
import sys
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

from flask import send_file
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

from flask_config import app


def get_pages_pdf(pdffile, filename, pagenrs, returntype):
  pdf = PdfFileReader(pdffile)
  pages = []
  
  for page in range(pdf.getNumPages()):
    if (page + 1) in pagenrs:
      pages.append(('page_{}.pdf'.format(page + 1), get_page_from_pdf(page, pdffile)))

  if (returntype == 'pdf'):
    memory_file = add_pages_to_pdf(pages)

  if (returntype == 'zip'):
    memory_file = add_pages_to_zip(pages)
    
  memory_file.seek(0)
  return send_file(memory_file, attachment_filename='{}.{}'.format(filename, returntype), as_attachment=True)

def get_page_from_pdf(pagenr, pdffile):
  page_as_bytesio = BytesIO()
  pdf_writer = PdfFileWriter()
  pdf_writer.addPage(PdfFileReader(pdffile).getPage(pagenr))
  
  pdf_writer.write(page_as_bytesio)
  page_as_bytesio.seek(0)
  return page_as_bytesio

def add_pages_to_pdf(files):
  mem_pdf = BytesIO()

  pdf_merger = PdfFileMerger()
  
  for f in files:
    pdf_merger.append(f[1])
  
  pdf_merger.write(mem_pdf)
  return mem_pdf

def add_pages_to_zip(files):
  mem_zip = BytesIO()
  zipped_pdfs = ZipFile(mem_zip, 'a', ZIP_DEFLATED)
  
  for f in files:
    zipped_pdfs.writestr(f[0], f[1].getbuffer())
    
  zipped_pdfs.close()
  return mem_zip
