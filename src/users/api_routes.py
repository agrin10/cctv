from flask import  jsonify ,request
from .controller import handle_login , handle_logout , handle_registration ,handle_add_users, handle_delete_user , handle_edit_user , get_user_accesses
from flask_login import login_user , logout_user
from flask_jwt_extended import jwt_required
from src.users import users_bp
from src.permissions import permission_required


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

@users_bp.route('/api/users', methods=['POST'])
@permission_required(['create'])
@jwt_required()
def api_add_users():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    camera_access = request.json.get('camera_access')
    zone_access = request.json.get('zone_access')
    user_access = request.json.get('user_access')

    all_permissions = camera_access + zone_access + user_access

    success, message, status = handle_add_users(username, password, email, all_permissions)
    if success:
        return jsonify(message=message, status=status) , 200
    return jsonify(message=message , status=status) , 400


@users_bp.route('/api/users' , methods=['PUT'])
@permission_required(['edit'])
@jwt_required()
def edit_users():
    username = request.json['username'] 
    new_username = request.json['new_username']
    password = request.json['password']
    new_password = request.json['new_password']
    new_email = request.json['new_email']

    success , message , status = handle_edit_user(username,new_username,password,new_password,new_email)
    if success:
        return jsonify(message=message , status=status)
    return jsonify(message=message , status=status)


@users_bp.route('/api/users' ,methods=['DELETE'])
@permission_required('delete')
@jwt_required()
def delete_users():
    username= request.args['username']
    success , message , status = handle_delete_user(username=username)
    if success:
        return jsonify(message=message , status=status)
    return jsonify(message=message , status=status)


@users_bp.route('/api/get')
@jwt_required()
def user_accesses():
    user_id = request.args.get("user_id")
    user_accesses = get_user_accesses(user_id)
    return jsonify(user_accesses=user_accesses) , 200