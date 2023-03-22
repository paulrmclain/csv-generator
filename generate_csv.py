import csv
import random
from utils import *

from faker import Faker
fake = Faker()

def generate_csv(filename, delimiter, quotechar, quoting, dialect, content):
    with open(filename, 'w', newline='\n') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=delimiter, quotechar=quotechar, quoting=quoting, dialect=dialect)
        csv_writer.writerows(content)


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

            # print('-------------')

            try:
                generated_value = method()
                # print('CALLED %s' % data_type['method'])
                # print('GOT %s' % generated_value)
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