#!/use/bin/python

import os, sys, calendar, time, datetime
from flask_config import app
from pathlib import Path

def allowed_file(filename, ALLOWED_EXTENSIONS):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_file_name(operation):
  filename = '{}_{}'.format(operation, str(time.time()))
  return str(filename)

def create_upload_dir(filename):
  currentYear = str(datetime.datetime.now().year)
  currentMonth = str(datetime.datetime.now().month)
  currentDay = str(datetime.datetime.now().day)
  new_dir = os.path.join(app.config['UPLOAD_FOLDER'], currentYear, currentMonth, currentDay, filename)
  Path(new_dir).mkdir(parents=True, exist_ok=True)
  return new_dir