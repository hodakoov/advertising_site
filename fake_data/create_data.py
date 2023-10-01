"""
Создание файла products.csv с фейковыми данными для заполнения БД
"""

import csv
import random
from faker import Faker

fake = Faker('ru_RU')


def get_fake_row():
    return [fake.text(max_nb_chars=20),
            fake.aba(),
            fake.date_time(),
            fake.url() + fake.uri_path(),
            fake.address(),
            random.randint(60000, 160000),
            fake.sentence(nb_words=30)
            ]


def generate_data(num_rows=50):
    with open('products.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        for _ in range(num_rows):
            writer.writerow(get_fake_row())


if __name__ == '__main__':
    generate_data()
