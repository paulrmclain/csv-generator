from generate_csv import *

from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, csv!'


@app.route('/test/generate/csv/<filename>/<rows>')
def test_generate_handler(filename, rows):
    args = request.args.items()
    test_generate_csv(filename, rows, args)
    return json.dumps(request.args)

@app.route('/test/types')
def test_get_faker_types():
    types = get_available_faker_types()
    return json.dumps(types)

@app.route('/generate/csv/<filename>/<rows>', methods=['POST'])
def generate_csv_handler(filename, rows):
    data_types = request.json
    content = test_generate_csv(filename, rows, request.json)
    return 'ok'
  
@app.route('/data/types')
def get_data_types():
    types = get_available_faker_types()
    return json.dumps(types)

