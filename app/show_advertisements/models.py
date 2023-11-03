from app.extensions import db
from app.user.models import User


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ad_id = db.Column(db.String(15), unique=True, nullable=False)
    ad_datetime = db.Column(db.DateTime, nullable=False)
    image_url = db.Column(db.String, nullable=True)
    address = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def __repr__(self):
        return f'Post "{self.title}" with id->{self.ad_id}'
