#!/use/bin/python

import os, sys, datetime, urllib.request
from flask_config import app
from flask import Flask, request, redirect, jsonify, Blueprint
from api_key_check import require_apikey
from global_functions import allowed_file, generate_file_name, create_upload_dir
from split_pdf_operations import split_pdf

split_pdf_route = Blueprint('split_pdf_route', __name__)

ALLOWED_EXTENSIONS = set(['pdf'])

@split_pdf_route.route('/api/v1/operations/splitpdf', methods=['POST'])
@require_apikey
def upload_file():
  # check if the post request has the file part
  if 'file' not in request.files:
    resp = jsonify({'message' : 'No file part in the request'})
    resp.status_code = 400
    return resp
  file = request.files['file']
  if file.filename == '':
    resp = jsonify({'message' : 'No file selected for uploading'})
    resp.status_code = 400
    return resp
  if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
    filename = generate_file_name('split')
    current_dir = create_upload_dir(filename)
    file.save(os.path.join(current_dir, '{}.pdf'.format(filename)))
    return split_pdf(current_dir, filename)
  else:
    resp = jsonify({'message' : 'Allowed file types are: pdf'})
    resp.status_code = 400
    return resp
