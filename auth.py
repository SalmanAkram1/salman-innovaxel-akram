# auth.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    # Save user to database (simulated)
    return jsonify({'message': 'User created successfully'}), 201
