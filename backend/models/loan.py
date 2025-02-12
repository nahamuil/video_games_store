from . import db
from datetime import datetime


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('video_game.id', ondelete='CASCADE'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    loan_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    return_date = db.Column(db.DateTime)
    price = db.Column(db.Float, nullable=False)

    # Updated relationships with back_populates
    game = db.relationship('VideoGame', back_populates='loans')
    customer = db.relationship('Customer')

    def to_dict(self):
        return {
            'id': self.id,
            'loan_date': self.loan_date.strftime('%Y-%m-%d %H:%M:%S'),
            'return_date': self.return_date.strftime('%Y-%m-%d %H:%M:%S') if self.return_date else None,
            'price': self.price,
            'game': self.game.to_dict() if self.game else None,
            'customer': self.customer.to_dict() if self.customer else None
        }
