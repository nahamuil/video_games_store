from . import db
from datetime import datetime


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('video_game.id', ondelete='CASCADE'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    loan_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)
    price = db.Column(db.Float, nullable=False)

    # Keep the existing relationship definitions
    game = db.relationship('VideoGame')
    customer = db.relationship('Customer')

    def to_dict(self):
        return {
            'id': self.id,
            'game_id': self.game_id,
            'customer_id': self.customer_id,
            'loan_date': self.loan_date.strftime('%Y-%m-%d %H:%M:%S'),
            'return_date': self.return_date.strftime('%Y-%m-%d %H:%M:%S') if self.return_date else None,
            'price': self.price
        }
