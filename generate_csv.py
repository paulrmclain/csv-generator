import csv
from faker import Faker
fake = Faker()

def generate_csv(delimiter, quotechar, quoting, dialect, content):
    with open('test.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=delimiter, quotechar=quotechar, quoting=quoting, dialect=dialect)
        csv_writer.writerows(content)


def test_generate_csv():
    Faker.seed(0)

    content = [[
        'name',
        'address',
        'phone_num',
        'occupation',
        'dob'
    ]]

    for i in range(10000):
        content.append([
            fake.name(),
            fake.address(),
            fake.phone_number(),
            fake.job(),
            fake.date_of_birth()
        ])

    generate_csv(',', '"', csv.QUOTE_MINIMAL, 'unix', content)