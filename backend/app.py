from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from models import db
from models.admin import Admin
from models.customer import Customer
from models.video_game import VideoGame
from models.loans import Loan

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gamestore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)
db.init_app(app)


# Admin Authentication
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        admin = Admin.query.filter_by(username=data['username']).first()

        if admin and admin.check_password(data['password']):
            access_token = create_access_token(identity=admin.id)
            return jsonify({'token': access_token}), 200
        return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# Customer Management
@app.route('/customers', methods=['GET'])
@jwt_required()
def get_customers():
    try:
        customers = Customer.query.all()
        return jsonify({
            'customers': [customer.to_dict() for customer in customers]
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/customers', methods=['POST'])
@jwt_required()
def add_customer():
    try:
        data = request.json
        new_customer = Customer(
            name=data['name'],
            email=data['email'],
            phone_number=data['phone_number']
        )
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({
            'message': 'Customer added successfully',
            'customer': new_customer.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


# Loan Management
@app.route('/games/<int:game_id>/loan', methods=['POST'])
@jwt_required()
def loan_game(game_id):
    try:
        data = request.json
        customer_id = data['customer_id']

        game = VideoGame.query.get_or_404(game_id)
        customer = Customer.query.get_or_404(customer_id)

        if game.is_loaned:
            return jsonify({'message': 'Game is already loaned'}), 400

        loan = Loan(
            customer_id=customer_id,
            game_id=game_id,
            price_charged=data.get('price_charged', game.price)
        )

        game.is_loaned = True
        game.quantity -= 1

        db.session.add(loan)
        db.session.commit()

        return jsonify({
            'message': 'Game loaned successfully',
            'loan': loan.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


# Initialize database with default admin
@app.before_first_request
def create_default_admin():
    with app.app_context():
        Admin.create_default_admin()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
