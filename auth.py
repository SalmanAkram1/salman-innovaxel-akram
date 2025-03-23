# auth.py
def is_admin(user):
    return user.role == 'admin'

@auth.route('/admin', methods=['GET'])
def admin_route():
    if not is_admin(current_user):
        return jsonify({'message': 'Access denied'}), 403
    return jsonify({'message': 'Welcome Admin'}), 200
