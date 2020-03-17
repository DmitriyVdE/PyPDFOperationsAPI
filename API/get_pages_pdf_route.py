#!/use/bin/python

import datetime
import os
import sys
import urllib.request

from flask import Blueprint, Flask, jsonify, redirect, request

from api_key_check import require_apikey
from flask_config import app
from get_pages_pdf_operations import get_pages_pdf
from global_functions import allowed_file, generate_file_name

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
    pagenrs = list(map(int, request.args.get('pages').split(',')))
    returntype = request.args.get('returntype').lower()
    return get_pages_pdf(file, filename, pagenrs, returntype)
  else:
    resp = jsonify({'message' : 'Allowed file types are: pdf'})
    resp.status_code = 400
    return resp
