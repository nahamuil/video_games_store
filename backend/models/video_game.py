from . import db


class VideoGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(500), nullable=False)

    # Updated relationship with back_populates
    loans = db.relationship('Loan', back_populates='game', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'publisher': self.publisher,
            'release_year': self.release_year,
            'genre': self.genre,
            'price': self.price,
            'quantity': self.quantity,
            'image_url': self.image_url
        }
