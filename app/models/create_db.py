from app.extensions import db
from app import create_app
from app.models.post import Post

# Запустить данный файл для создания БД и таблицы post
db.create_all(app=create_app())
