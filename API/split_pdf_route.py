import os, sys, urllib.request
from flask_config import app
from flask import Flask, request, redirect, jsonify, Blueprint
from werkzeug.utils import secure_filename
from split_pdf_operations import generate_file_name, split_pdf

split_pdf_route = Blueprint('split_pdf_route', __name__)

ALLOWED_EXTENSIONS = set(['pdf'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@split_pdf_route.route('/api/v1/operations/splitpdf', methods=['POST'])
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
	if file and allowed_file(file.filename):
		filename = generate_file_name()
		file.save(os.path.join(app.config['UPLOAD_FOLDER'] + filename.split('.')[0], filename))
		return split_pdf(app.config['UPLOAD_FOLDER'] + filename.split('.')[0] + '/' + filename)
	else:
		resp = jsonify({'message' : 'Allowed file types are: pdf'})
		resp.status_code = 400
		return resp