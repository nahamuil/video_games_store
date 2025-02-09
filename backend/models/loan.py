from . import db
from datetime import datetime


class Loan(db.Model):
    __tablename__ = 'loan'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('video_game.id'), nullable=False)  # Updated foreign key reference
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    loan_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)
    price = db.Column(db.Float, nullable=False)

    game = db.relationship('VideoGame', backref=db.backref('loans', lazy=True))
    customer = db.relationship('Customer', backref=db.backref('loans', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'game_id': self.game_id,
            'customer_id': self.customer_id,
            'game_title': self.game.title,
            'customer_name': self.customer.name,
            'loan_date': self.loan_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'price': self.price
        }
