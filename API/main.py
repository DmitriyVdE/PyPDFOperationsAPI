#!/use/bin/python

import shutil

from flask import Flask, jsonify, request

from api_key_check import require_apikey
from flask_config import app
from get_pages_pdf_route import get_pages_pdf_route
from merge_pdf_route import merge_pdf_route
from rotate_pdf_route import rotate_pdf_route
from split_pdf_route import split_pdf_route

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

@app.errorhandler(404)
def page_not_found(e):
  resp = jsonify({'message' : 'Invalid route.'})
  resp.status_code = 404
  return resp

if __name__ == "__main__":
    app.run(port=5001)
