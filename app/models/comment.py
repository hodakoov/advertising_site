from datetime import datetime
from sqlalchemy.orm import relationship

from app.extensions import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    post_id = db.Column(
        db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), index=True
    )
    author_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), index=True
    )
    post = relationship('Post', backref='comments')
    user = relationship('User', backref='comments')

    def __repr__(self):
        return f'<Comment {self.id}>'
