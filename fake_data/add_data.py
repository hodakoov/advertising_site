"""
Заполнение БД фейковыми данными из файла products.csv (полученного при помощи create_data.py)
Прим. БД должна быть создана
"""

import csv
from datetime import datetime

from app.models.post import Post
from app.extensions import db
from app import create_app

app = create_app()


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['title', 'ad_id', 'ad_datetime', 'image_url',
                  'address', 'price', 'description']
        reader = csv.DictReader(f, fields, delimiter=';')
        for row in reader:
            row['ad_datetime'] = datetime.strptime(row['ad_datetime'], '%Y-%m-%d %H:%M:%S')
            save_salary_data(row)


def save_salary_data(row):
    post = Post(title=row['title'], ad_id=row['ad_id'],
                ad_datetime=row['ad_datetime'],
                image_url=row['image_url'], address=row['address'],
                price=row['price'], description=row['description'])
    db.session.add(post)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        read_csv('products.csv')
