#!/use/bin/python

import os, sys, datetime, urllib.request
from flask_config import app
from flask import Flask, request, redirect, jsonify, Blueprint
from api_key_check import require_apikey
from global_functions import allowed_file, generate_file_name, create_upload_dir
from get_pages_pdf_operations import get_pages_pdf

get_pages_pdf_route = Blueprint('get_pages_pdf_route', __name__)

ALLOWED_EXTENSIONS = set(['pdf'])
RETURN_TYPES = set(['pdf', 'zip'])

@get_pages_pdf_route.route('/api/v1/operations/getpagespdf', methods=['POST'])
@require_apikey
def upload_file():
  if 'pages' not in request.args:
    resp = jsonify({'message' : 'No pages part in the request'})
    resp.status_code = 400
    return resp
  if 'returntype' not in request.args or request.args['returntype'].lower() not in RETURN_TYPES:
    resp = jsonify({'message' : 'No or invalid return type in the request'})
    resp.status_code = 400
    return resp
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
    filename = generate_file_name('get_pages')
    current_dir = create_upload_dir(filename)
    file.save(os.path.join(current_dir, '{}.pdf'.format(filename)))
    pages = list(map(int, request.args.get('pages').split(',')))
    returntype = request.args.get('returntype').lower()
    return get_pages_pdf(current_dir, filename, pages, returntype)
  else:
    resp = jsonify({'message' : 'Allowed file types are: pdf'})
    resp.status_code = 400
    return resp
