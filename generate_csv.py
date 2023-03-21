import csv
import random
import json
from utils import *

from faker import Faker
fake = Faker()

def generate_csv(filename, delimiter, quotechar, quoting, dialect, content):
    with open(filename, 'w', newline='\n') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=delimiter, quotechar=quotechar, quoting=quoting, dialect=dialect)
        csv_writer.writerows(content)


def test_generate_csv(filename, num_rows, args):
    Faker.seed(random.randrange(0, 100))

    content = []
    header = []
    functions = []

    for key, value in args:
        header.append(key)
        functions.append(value)

    content.append(header)

    for i in range(int(num_rows)):
        row = []
        for f in functions:
            match f:
                case 'name':
                    row.append(fake.name())
                case 'address':
                    row.append(fake.address())
                case 'phone_number':
                    row.append(fake.phone_number())
                case 'job':
                    row.append(fake.job())
                case 'date_of_birth': 
                    row.append(fake.date_of_birth())
                case 'email':
                    row.append(fake.email())
                case _:
                    None

        content.append(row)

    generate_csv(filename, ',', '"', csv.QUOTE_MINIMAL, 'unix', content)


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