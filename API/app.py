from flask import Flask
from flask import request, jsonify

UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config["DEBUG"] = True

@app.route('/')
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
