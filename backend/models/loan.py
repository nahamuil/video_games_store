from . import db
from datetime import datetime


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('video_game.id'), nullable=False)
    loan_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)
    price_charged = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'game_id': self.game_id,
            'loan_date': self.loan_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'price_charged': self.price_charged
        }
