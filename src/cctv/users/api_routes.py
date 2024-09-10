from flask import  jsonify ,request
from .controller import handle_login , handle_logout , handle_registration
from flask_login import login_user , logout_user
from flask_jwt_extended import jwt_required
from src.cctv.users import users_bp



@users_bp.route('/api/register', methods=['POST'])
def api_register():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    success, message = handle_registration(username, password, email)
    return jsonify(message=message, success=success)
    
@users_bp.route('/api/login', methods=['POST'])
def api_login():
    username = request.json['username']
    password = request.json['password']
    user, success, message,  response = handle_login(username, password)
    if success:
        login_user(user)
        return response
    else:
        return jsonify(message=message, success=success), 401


    
@users_bp.route('/api/logout', methods=['POST'])
@jwt_required()
def api_logout():
    logout_user()
    response = handle_logout()
    return response
