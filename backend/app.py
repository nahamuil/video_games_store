from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import re
from models import db
from models.admin import Admin
from models.customer import Customer
from models.video_game import VideoGame
from models.loan import Loan

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gamestore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


def init_app():
    with app.app_context():
        db.create_all()
        # Check if admin exists, if not create default admin
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(username='admin', password='admin123')
            db.session.add(admin)
            db.session.commit()


# Helper Functions for Validation

def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(pattern, email):
        return True
    return False


def validate_phone(phone):
    # Example for validating phone number (format: +1 (234) 567-890)
    pattern = r'^\+?(\d{1,3})?[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}$'
    if re.match(pattern, phone):
        return True
    return False


def validate_year(year):
    current_year = datetime.now().year
    if year and 1900 <= year <= current_year:
        return True
    return False


def validate_genre(genre):
    valid_genres = ['Action', 'Adventure', 'RPG', 'Sports', 'Shooter', 'Strategy', 'Puzzle', 'Simulation']
    if genre in valid_genres:
        return True
    return False


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    admin = Admin.query.filter_by(username=data['username']).first()

    if not admin:
        return jsonify({
            'success': False,
            'message': 'Invalid username'
        }), 401

    if admin.password != data['password']:
        return jsonify({
            'success': False,
            'message': 'Incorrect password'
        }), 401

    return jsonify({
        'success': True,
        'message': 'Login successful'
    }), 200


@app.route('/api/customers', methods=['GET', 'POST'])
def handle_customers():
    if request.method == 'GET':
        customers = Customer.query.all()
        return jsonify([c.to_dict() for c in customers])

    data = request.json

    # Validation for email, phone
    if not validate_email(data['email']):
        return jsonify({'error': 'Invalid email address'}), 400
    if not validate_phone(data['phone']):
        return jsonify({'error': 'Invalid phone number'}), 400

    customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_dict()), 201


@app.route('/api/games', methods=['GET', 'POST'])
def handle_games():
    if request.method == 'GET':
        games = VideoGame.query.all()
        return jsonify([g.to_dict() for g in games])

    data = request.json

    # Validation for release year and genre
    if not validate_year(data['release_year']):
        return jsonify({'error': 'Invalid year for the game'}), 400
    if not validate_genre(data['genre']):
        return jsonify({'error': 'Invalid game genre'}), 400

    game = VideoGame(
        title=data['title'],
        publisher=data['publisher'],
        release_year=data['release_year'],
        genre=data['genre'],
        price=data['price'],
        quantity=data['quantity']
    )
    db.session.add(game)
    db.session.commit()
    return jsonify(game.to_dict()), 201


@app.route('/api/loans', methods=['GET', 'POST'])
def handle_loans():
    if request.method == 'GET':
        loans = Loan.query.filter_by(return_date=None).all()
        return jsonify([{
            'id': l.id,
            'loan_date': l.loan_date.strftime('%Y-%m-%d %H:%M:%S'),
            'return_date': l.return_date.strftime('%Y-%m-%d %H:%M:%S') if l.return_date else None,
            'price': l.price,
            'game': {
                'id': l.game.id,
                'title': l.game.title,
                'publisher': l.game.publisher
            },
            'customer': {
                'id': l.customer.id,
                'name': l.customer.name,
                'email': l.customer.email
            }
        } for l in loans])

    data = request.json
    game = VideoGame.query.get_or_404(data['game_id'])
    customer = Customer.query.get_or_404(data['customer_id'])

    if game.quantity < 1:
        return jsonify({'error': 'Game not available'}), 400

    # Create loan with the game's price
    loan = Loan(
        game_id=data['game_id'],
        customer_id=data['customer_id'],
        loan_date=datetime.utcnow(),
        price=game.price  # Get the price from the game
    )
    game.quantity -= 1

    try:
        db.session.add(loan)
        db.session.commit()
        return jsonify({
            'id': loan.id,
            'loan_date': loan.loan_date.strftime('%Y-%m-%d %H:%M:%S'),
            'price': loan.price,
            'game': {
                'id': loan.game.id,
                'title': loan.game.title
            },
            'customer': {
                'id': loan.customer.id,
                'name': loan.customer.name
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/loans/<int:loan_id>/return', methods=['POST'])
def return_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    if loan.return_date:
        return jsonify({'error': 'Loan already returned'}), 400

    loan.return_date = datetime.utcnow()
    loan.game.quantity += 1
    db.session.commit()
    return jsonify(loan.to_dict())


# Add this new route to your Flask app (app.py)
@app.route('/api/games/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    game = VideoGame.query.get_or_404(game_id)

    # Check if game has any active loans
    active_loans = Loan.query.filter_by(game_id=game_id, return_date=None).first()
    if active_loans:
        return jsonify({'error': 'Cannot delete game with active loans'}), 400

    try:
        db.session.delete(game)
        db.session.commit()
        return jsonify({'message': 'Game deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    init_app()  # Call initialization function before running the app
    app.run(debug=True)
