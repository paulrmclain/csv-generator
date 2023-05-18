from generate_csv import *

import json
import jsonpickle

from dotenv import dotenv_values
import google.cloud.logging

from flask import Flask, render_template, request, send_file, redirect
app = Flask(__name__)

client = google.cloud.logging.Client()
client.setup_logging()

import logging

config = dotenv_values("config.env")

@app.route("/")
def index_page():
    return render_template('index.html')

@app.route('/test/generate/csv/<filename>/<rows>')
def test_generate_handler(filename, rows):
    args = request.args.items()
    test_generate_csv(filename, rows, args)
    return json.dumps(request.args)

@app.route('/test/types')
def test_get_faker_types():
    types = get_available_faker_types()
    return json.dumps(types)

@app.route('/api/generate/csv/<filename>/<rows>/<delimiter>', methods=['POST'])
def generate_csv_handler(filename, rows, delimiter):
    logging.info('In generate_csv_handler with filename %s and delimiter %s' % (filename, delimiter))
    data_types = request.get_json()
    content = init_generate_csv(config['PROJECT_URL'], filename, rows, data_types, delimiter)
    response_json = jsonpickle.encode(content)
    return response_json
  
@app.route('/api/data/types')
def get_data_types():
    types = get_available_faker_types()
    return json.dumps(types)
    
@app.route('/download/<uuid>')
def download_csv(uuid):
    url = 'https://storage.googleapis.com/' + config['PROJECT_URL'] + '/' + uuid
    return redirect(url)

@app.route('/test/envs')
def test_envs():
    logging.info(config)
    return json.dumps(config)
