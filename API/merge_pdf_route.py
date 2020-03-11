#!/use/bin/python

import os, sys, datetime, urllib.request
from flask_config import app
from flask import Flask, request, redirect, jsonify, Blueprint
from api_key_check import require_apikey
from global_functions import allowed_file, generate_file_name, create_upload_dir
from merge_pdf_operations import merge_pdf

merge_pdf_route = Blueprint('merge_pdf_route', __name__)

ALLOWED_EXTENSIONS = set(['zip'])

@merge_pdf_route.route('/api/v1/operations/mergepdf', methods=['POST'])
@require_apikey
def upload_file():
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
    filename = generate_file_name('merge')
    current_dir = create_upload_dir(filename)
    file.save(os.path.join(current_dir, '{}.zip'.format(filename)))
    return merge_pdf(current_dir, filename)
  else:
    resp = jsonify({'message' : 'Allowed file types are: pdf'})
    resp.status_code = 400
    return resp
