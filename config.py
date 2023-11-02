import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # URI используемая для подключения к базе данных
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SCRAPER_INITIAL_URL = 'https://www.avito.ru/moskva/telefony/mobilnye_telefony/apple-ASgBAgICAkS0wA3OqzmwwQ2I_Dc?cd=1'  # noqa: E501
    SCRAPER_PAGE_LIMIT = 1
    SCRAPER_DELAY_LIMIT = 20

    SECRET_KEY = '3c2b5a460cf5a395731dd6e98a5690cb'

    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
