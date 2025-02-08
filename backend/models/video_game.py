from . import db


class VideoGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    creator = db.Column(db.String(200), nullable=False)  # Game developer/publisher
    year_published = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    is_loaned = db.Column(db.Boolean, default=False)
    loans = db.relationship('Loan', backref='video_game', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'creator': self.creator,
            'year_published': self.year_published,
            'genre': self.genre,
            'price': self.price,
            'quantity': self.quantity,
            'is_loaned': self.is_loaned
        }
