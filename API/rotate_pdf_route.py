#!/use/bin/python

import os, sys, datetime, urllib.request
from flask_config import app
from flask import Flask, request, redirect, jsonify, Blueprint
from api_key_check import require_apikey
from global_functions import allowed_file, generate_file_name, create_upload_dir
from rotate_pdf_operations import rotate_pdf

rotate_pdf_route = Blueprint('rotate_pdf_route', __name__)

ALLOWED_EXTENSIONS = set(['pdf'])
AMOUNT_VALUES = set(['1', '2', '3'])

@rotate_pdf_route.route('/api/v1/operations/rotatepdf', methods=['POST'])
@require_apikey
def upload_file():
  if 'amount' not in request.args or request.args['amount'] not in AMOUNT_VALUES:
    resp = jsonify({'message' : 'No or invalid amount in the request'})
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
    filename = generate_file_name('rotate')
    current_dir = create_upload_dir(filename)
    file.save(os.path.join(current_dir, '{}.pdf'.format(filename)))
    amount = request.args.get('amount')
    return rotate_pdf(current_dir, filename, amount)
  else:
    resp = jsonify({'message' : 'Allowed file types are: pdf'})
    resp.status_code = 400
    return resp
