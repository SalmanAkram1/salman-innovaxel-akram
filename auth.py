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
# routes.py
@app.route('/share/<short_code>', methods=['GET'])
def share_url(short_code):
    url_data = URL.query.filter_by(short_code=short_code).first()
    if url_data:
        # Share URL logic (e.g., via email)
        return jsonify({'message': f"Shared URL: {url_data.url}"}), 200
    return jsonify({'error': 'URL not found'}), 404

