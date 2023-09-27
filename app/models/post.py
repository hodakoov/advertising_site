from app.extensions import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ad_number = db.Column(db.String(15), unique=True, nullable=False)
    ad_datetime = db.Column(db.DateTime, nullable=False)
    url_on_foto = db.Column(db.String, unique=True, nullable=True)
    address = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=True)
    Description = db.Column(db.Text, nullable=False)
