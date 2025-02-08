from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from models import db
from models.user import User
from models.video_game import VideoGame
from models.loans import Loan

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gamestore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize extensions
jwt = JWTManager(app)
db.init_app(app)


# Authentication routes
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists'}), 400

        user = User(
            username=data['username'],
            password=generate_password_hash(data['password'])
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        user = User.query.filter_by(username=data['username']).first()

        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            return jsonify({'token': access_token}), 200
        return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'message': f'Login failed: {str(e)}'}), 500


# Game management routes
@app.route('/games', methods=['GET'])
@jwt_required()
def get_games():
    try:
        games = VideoGame.query.all()
        return jsonify({
            'message': 'Games retrieved successfully',
            'games': [game.to_dict() for game in games]
        }), 200
    except Exception as e:
        return jsonify({'message': f'Failed to retrieve games: {str(e)}'}), 500


@app.route('/games', methods=['POST'])
@jwt_required()
def add_game():
    try:
        data = request.json
        new_game = VideoGame(
            title=data['title'],
            creator=data['creator'],
            year_published=data['year_published'],
            genre=data['genre'],
            price=data['price'],
            quantity=data.get('quantity', 1)
        )
        db.session.add(new_game)
        db.session.commit()
        return jsonify({
            'message': 'Game added successfully',
            'game': new_game.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to add game: {str(e)}'}), 500


@app.route('/games/<int:game_id>', methods=['PUT'])
@jwt_required()
def update_game(game_id):
    try:
        game = VideoGame.query.get_or_404(game_id)
        data = request.json

        game.title = data.get('title', game.title)
        game.creator = data.get('creator', game.creator)
        game.year_published = data.get('year_published', game.year_published)
        game.genre = data.get('genre', game.genre)
        game.price = data.get('price', game.price)
        game.quantity = data.get('quantity', game.quantity)

        db.session.commit()
        return jsonify({
            'message': 'Game updated successfully',
            'game': game.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to update game: {str(e)}'}), 500


@app.route('/games/<int:game_id>', methods=['DELETE'])
@jwt_required()
def delete_game(game_id):
    try:
        game = VideoGame.query.get_or_404(game_id)
        if game.is_loaned:
            return jsonify({'message': 'Cannot delete a game that is currently loaned'}), 400

        db.session.delete(game)
        db.session.commit()
        return jsonify({'message': 'Game deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to delete game: {str(e)}'}), 500


# Loan management routes
@app.route('/games/<int:game_id>/loan', methods=['POST'])
@jwt_required()
def loan_game(game_id):
    try:
        game = VideoGame.query.get_or_404(game_id)
        user_id = get_jwt_identity()

        if game.is_loaned:
            return jsonify({'message': 'Game is already loaned'}), 400
        if game.quantity < 1:
            return jsonify({'message': 'Game is out of stock'}), 400

        # Create new loan record
        loan = Loan(
            user_id=user_id,
            game_id=game_id,
            loan_date=datetime.utcnow()
        )
        game.is_loaned = True
        game.quantity -= 1

        db.session.add(loan)
        db.session.commit()

        return jsonify({
            'message': 'Game loaned successfully',
            'loan': {
                'game_id': game_id,
                'loan_date': loan.loan_date.isoformat()
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to loan game: {str(e)}'}), 500


@app.route('/games/<int:game_id>/return', methods=['POST'])
@jwt_required()
def return_game(game_id):
    try:
        game = VideoGame.query.get_or_404(game_id)
        user_id = get_jwt_identity()

        loan = Loan.query.filter_by(
            game_id=game_id,
            user_id=user_id,
            return_date=None
        ).first()

        if not loan:
            return jsonify({'message': 'No active loan found for this game'}), 404

        loan.return_date = datetime.utcnow()
        game.is_loaned = False
        game.quantity += 1

        db.session.commit()
        return jsonify({'message': 'Game returned successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to return game: {str(e)}'}), 500


@app.route('/loans', methods=['GET'])
@jwt_required()
def get_loans():
    try:
        user_id = get_jwt_identity()
        active_loans = Loan.query.filter_by(
            user_id=user_id,
            return_date=None
        ).all()

        loans_data = [{
            'game_id': loan.game_id,
            'loan_date': loan.loan_date.isoformat(),
            'game_title': loan.video_game.title
        } for loan in active_loans]

        return jsonify({
            'message': 'Loans retrieved successfully',
            'loans': loans_data
        }), 200
    except Exception as e:
        return jsonify({'message': f'Failed to retrieve loans: {str(e)}'}), 500


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'message': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'message': 'Internal server error'}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
