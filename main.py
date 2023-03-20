from generate_csv import *

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, csv!'


@app.route('/test/generate/csv')
def test_generate_handler():
    test_generate_csv()
    return 'CSV generated?'