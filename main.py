from generate_csv import *

import json
import jsonpickle

from dotenv import dotenv_values
# from io import BytesIO

from flask import Flask, render_template, request, send_file, redirect
app = Flask(__name__)

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

@app.route('/api/generate/csv/<filename>/<rows>', methods=['POST'])
def generate_csv_handler(filename, rows):
    data_types = request.get_json()
    config = dotenv_values("config.env")
    # print(data_types)
    print(config['CLOUD_STORAGE_URL'])
    print('-------')
    content = init_generate_csv(config['CLOUD_STORAGE_URL'], filename, rows, data_types)
    response_json = jsonpickle.encode(content)
    return response_json
  
@app.route('/api/data/types')
def get_data_types():
    types = get_available_faker_types()
    return json.dumps(types)
    
@app.route('/download/<uuid>')
def download_csv(uuid):
    url = 'https://storage.googleapis.com/csv-generator-381519.appspot.com/' + uuid
    return redirect(url)

@app.route('/test/envs')
def test_envs():
    config = dotenv_values("config.env")
    print(config)
    return json.dumps(config)
