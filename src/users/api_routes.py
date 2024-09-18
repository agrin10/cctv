from flask import  jsonify ,request
from .controller import handle_login , handle_logout , handle_registration  , handle_add_user , handle_delete_user , handle_edit_user
from flask_login import login_user , logout_user
from flask_jwt_extended import jwt_required
from src.users import users_bp



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

@users_bp.route('/api/users' , methods=['POST'])
def api_add_users():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    module_name = request.json.get("module_name")
    permossions = request.json['permissions']
    # print('\n\n')
    # print(permossions)
    # print('\n\n')
    # print(module_name)
    success , message , status = handle_add_user(username=username , password=password , email=email , module_name=module_name, permissions=permossions)
    if success:
        return jsonify(message=message , status=status)
    return jsonify(message=message , status=status)

@users_bp.route('/api/users' , methods=['PUT'])
def edit_users():
    username = request.json['username'] 
    new_username = request.json['new_username']
    new_password = request.json['new_password']
    password = request.json['password']
    new_email = request.json['new_email']

    success , message , status = handle_edit_user(username,new_username,password,new_password,new_email)
    if success:
        return jsonify(message=message , status=status)
    return jsonify(message=message , status=status)


@users_bp.route('/api/users' ,methods=['DELETE'])
def delete_users():
    username= request.args['username']
    success , message , status = handle_delete_user(username=username)
    if success:
        return jsonify(message=message , status=status)
    return jsonify(message=message , status=status)

