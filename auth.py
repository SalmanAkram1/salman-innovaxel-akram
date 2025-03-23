from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_login import current_user  # Import current_user for user sessions

auth = Blueprint('auth', __name__)

# Signup route
@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    # Save user to database (simulated)
    return jsonify({'message': 'User created successfully'}), 201

# Login route
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # Simulate checking credentials
    if check_password_hash(data['password'], 'hashed_password_from_db'):
        token = create_access_token(identity=data['username'])
        return jsonify({'access_token': token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

# Admin route with RBAC
def is_admin(user):
    return user.role == 'admin'

@auth.route('/admin', methods=['GET'])
def admin_route():
    if not is_admin(current_user):
        return jsonify({'message': 'Access denied'}), 403
    return jsonify({'message': 'Welcome Admin'}), 200
