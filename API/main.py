#!/use/bin/python

import shutil
from flask import Flask
from flask import request, jsonify
from flask_config import app
from api_key_check import require_apikey
from split_pdf_route import split_pdf_route
from get_pages_pdf_route import get_pages_pdf_route
from merge_pdf_route import merge_pdf_route
from rotate_pdf_route import rotate_pdf_route

app.register_blueprint(split_pdf_route)
app.register_blueprint(get_pages_pdf_route)
app.register_blueprint(merge_pdf_route)
app.register_blueprint(rotate_pdf_route)

@app.route('/')
@app.route('/api')
@app.route('/home')
@app.route('/index')
def home():
  resp = jsonify({'message' : 'Welcome to the File Operations API v1.'})
  resp.status_code = 200
  return resp

@app.route('/api/v1/clearuploads', methods=['DELETE'])
@require_apikey
def clear_uplaods():
  try:
    shutil.rmtree('uploads/')
    resp = jsonify({'message' : 'Uploas folder cleared.'})
    resp.status_code = 200
  except:
    resp = jsonify({'error' : 'There was an error clearing the uploads folder.'})
    resp.status_code = 500
    
  return resp

@app.errorhandler(404)
def page_not_found(e):
  resp = jsonify({'message' : 'Invalid route.'})
  resp.status_code = 404
  return resp

if __name__ == "__main__":
    app.run(port=5001)
