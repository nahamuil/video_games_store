from . import db


class VideoGame(db.Model):
    __tablename__ = 'video_game'  # Explicitly set table name
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    publisher = db.Column(db.String(200), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'publisher': self.publisher,
            'release_year': self.release_year,
            'genre': self.genre,
            'price': self.price,
            'quantity': self.quantity,
            'available': self.quantity > 0
        }
