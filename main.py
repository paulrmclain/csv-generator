from generate_csv import *

from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, csv!'


@app.route('/test/generate/csv/<filename>/<num_rows>')
def test_generate_handler(filename, num_rows):
    args = request.args.items()
    test_generate_csv(filename, num_rows, args)
    return json.dumps(request.args)