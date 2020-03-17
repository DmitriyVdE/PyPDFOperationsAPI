#!/use/bin/python

import os
import sys
from io import BytesIO
from pathlib import Path

from flask import send_file
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

from flask_config import app


def rotate_pdf(pdffile, filename, rotation):
  memory_file = rotate_pdf_pages(pdffile, rotation)
  memory_file.seek(0)
  return send_file(memory_file, attachment_filename='{}.pdf'.format(filename), as_attachment=True)

def rotate_pdf_pages(pdffile, rotation):
  mem_pdf = BytesIO()
  pdf_reader = PdfFileReader(pdffile)
  pdf_merger = PdfFileMerger()
  
  for page in range(pdf_reader.getNumPages()):
    if rotation == '1':
      rotated_page = pdf_reader.getPage(page).rotateClockwise(90)
    if rotation == '2':
      rotated_page = pdf_reader.getPage(page).rotateClockwise(180)
    if rotation == '3':
      rotated_page = pdf_reader.getPage(page).rotateCounterClockwise(90)
    page_as_bytesio = BytesIO()
    pdf_writer = PdfFileWriter()
    pdf_writer.addPage(rotated_page)
    pdf_writer.write(page_as_bytesio)
    page_as_bytesio.seek(0)
    pdf_merger.append(page_as_bytesio)

  pdf_merger.write(mem_pdf)
  return mem_pdf
