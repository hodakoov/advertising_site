import csv
import random

from faker import Faker

from app.models.post import Post
from app.extensions import db
from app import create_app


def get_fake_row():
    fake = Faker('ru_RU')
    return [
        fake.text(max_nb_chars=20),
        fake.aba(),
        fake.date_time(),
        fake.url() + fake.uri_path(),
        fake.address(),
        random.randint(60000, 160000),
        fake.sentence(nb_words=30)
    ]


def generate_data(num_rows=50):
    for _ in range(num_rows):
        row = get_fake_row()
        yield row


def save_to_csv(f, row):
    writer = csv.writer(f, delimiter=';')
    writer.writerow(row)


def save_to_db(row):
    post = Post(
        title=row[0],
        ad_id=row[1],
        ad_datetime=row[2],
        image_url=row[3],
        address=row[4],
        price=row[5],
        description=row[6])
    db.session.add(post)
    db.session.commit()


if __name__ == "__main__":
    write_to_db = input('Записать данные в базу данных (y/n):\n')
    if write_to_db.lower() in 'y':
        app = create_app()
        with app.app_context():
            for row in generate_data():
                save_to_db(row)
    else:
        with open('fake_data.csv', 'w', encoding='utf-8') as f:
            for row in generate_data():
                save_to_csv(f, row)