import io
import csv
import random
from utils import *

from google.cloud import storage

from faker import Faker
fake = Faker()

def write_to_gcs(filename, csv_content):
    
    storage_client = storage.Client()
    bucket = storage_client.bucket('csv-generator-381519.appspot.com')
    blob = bucket.blob(filename)
    blob.upload_from_string(data=csv_content, content_type='text/csv')

def generate_csv(filename, delimiter, quotechar, quoting, dialect, content):
    output = io.StringIO()
    csv_writer = csv.writer(output, delimiter=delimiter, quotechar=quotechar, quoting=quoting, dialect=dialect)
    csv_writer.writerows(content)
    csv_content = output.getvalue()

    write_to_gcs(filename, csv_content)
    
def init_generate_csv(filename, rows, data_types):
    Faker.seed(random.randrange(0, 100))

    content = []
    header = []
    functions = []

    for i in range(int(rows)):
        row = []
        for data_type in data_types:
            generated_value = None
            method = getattr(fake, data_type['method'])

            try:
                generated_value = method()
            except Exception as e:
                print('TRIED TO CALL %s' % data_type['method'])
                generated_value = None
                print('generated_value is now %s' % generated_value)
                print(e)

            if generated_value is not None:
                row.append(generated_value)
                if data_type['label'] not in header:
                    header.append(data_type['label'])

        content.append(row)

    content.insert(0, header)

    generate_csv(filename, ',', '"', csv.QUOTE_MINIMAL, 'unix', content)

    return content

def get_available_faker_types():
    types_and_labels = []
    types = get_members(fake)

    for t in types:
        label = convert_to_sentence(convert_to_camel(t))
        types_and_labels.append({
            'label': label,
            'method': t
        })

    return types_and_labels