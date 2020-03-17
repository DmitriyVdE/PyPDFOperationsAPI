#!/use/bin/python

import os
import sys
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

from flask import send_file
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

from flask_config import app


def merge_pdf(zipfile, filename):
  pages = extract_pages_from_zip(zipfile)
  memory_file = add_pages_to_pdf(pages)
  memory_file.seek(0)
  return send_file(memory_file, attachment_filename='{}.{}'.format(filename, 'pdf'), as_attachment=True)

def extract_pages_from_zip(zipfile):
  pages = []

  with ZipFile(zipfile, 'r')as zipObj:
    list_of_file_names = zipObj.namelist()
    for file_name_in_zip in list_of_file_names:
      if file_name_in_zip.endswith('.pdf'):
        with BytesIO(zipObj.read(file_name_in_zip)) as pdf_io_file:
          actual_page = PdfFileReader(pdf_io_file)
          for page in range(actual_page.getNumPages()):
            page_as_bytesio = BytesIO()
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(actual_page.getPage(page))
            pdf_writer.write(page_as_bytesio)
            page_as_bytesio.seek(0)
            pages.append(page_as_bytesio)

  return pages

def add_pages_to_pdf(pages):
  mem_pdf = BytesIO()

  pdf_merger = PdfFileMerger()
  
  for page in pages:
    pdf_merger.append(page)
  
  pdf_merger.write(mem_pdf)
  return mem_pdf
