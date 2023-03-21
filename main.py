from generate_csv import *

import json

from flask import Flask, render_template, request
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
    # print(request.get_data())
    data_types = request.get_json()
    print(data_types)
    content = init_generate_csv(filename, rows, request.json)
    return 'got it'
  
@app.route('/api/data/types')
def get_data_types():
    types = get_available_faker_types()
    return json.dumps(types)

