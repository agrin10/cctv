from flask import redirect, url_for, render_template, request, flash , jsonify
from flask_login import login_user, logout_user
import os
from flask_jwt_extended import jwt_required
from .controller import handle_login, handle_registration, handle_logout, handle_add_users, handle_delete_user, handle_edit_user, user_list 
from src.users import users_bp
from .model import Accesses, Permissions, UserAccess, Module, Users
from src.permissions import permission_required
from src.camera.model import Camera
from src.zone.model import Zone
from src.users.schema import AddUserSchema , EditUserSchema
from marshmallow import ValidationError



@users_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        success, message = handle_registration(username, password, email)
        if success:
            flash(message=message)
            return redirect(url_for('users.login'))
        else:
            flash(message=message)
            return redirect(url_for('users.register'))
    return render_template('authentication.html' , side_menu= True)


@users_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # TODO user is not identify
        user, success, message, response = handle_login(username, password)

        if success:
            login_user(user)
            flash(message=message)

            response.headers['Location'] = url_for('web.home_page')
            response.status_code = 302

            return response

        flash(message=message)
        return redirect(url_for('users.login'))
    return render_template('authentication.html')


@users_bp.route('/logout')
@jwt_required()
def logout():
    logout_user()

    response = handle_logout()

    response.headers['Location'] = url_for('users.login')
    response.status_code = 302
    return response



@users_bp.route('/')
@jwt_required()
@permission_required(['view'])
def user_manage():
    list_users = Users.query.all()
    accesses = Accesses.query.join(Permissions).join(Module).all()
    camera = Camera.query.all()
    zone = Zone.query.all()
    # pagination
    page = request.args.get('page', 1, type=int)  
    per_page = 10  
    users = Users.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('user-manage.html', users_list=list_users, accesses=accesses, cameras= camera , zones= zone , users=users.items , pagination=users)

    
@users_bp.route('/delete-users/<username>', methods=["DELETE"])
@permission_required(['delete'])
@jwt_required()
def delete_user(username):
    success, message, status = handle_delete_user(username)
    if success:
        return ({'success': True, 'message': message}), 200
    else:
        return ({'success': False, 'message': message}), status


@users_bp.route('/', methods=["POST"])
@permission_required(['create'])
@jwt_required()
def add_user():
    schema = AddUserSchema()
    try:
        if request.is_json:
            form_data = request.get_json()
        else:
            form_data = request.form.to_dict(flat=True)
        form_data["camera_access"] = request.form.getlist('camera_access')
        form_data["zone_access"] = request.form.getlist('zone_access')
        form_data["user_access"] = request.form.getlist('user_access')
        form_data["access_to_cameras"] = request.form.getlist('access_to_cameras')
        form_data["access_to_zones"] = request.form.getlist('access_to_zones')

        data =schema.load(form_data)
    except ValidationError as err:
        return jsonify({"success": False, "errors": err.messages}), 400
        
            
    all_permissions = data["camera_access"] + data["zone_access"] + data["user_access"]

    success , message , status = handle_add_users(
        firstname=data["firstName"], 
        lastname=data["lastName"],
        username=data["username"],
        password=data["password"],
        permission_names=all_permissions,
        camera_ids=data["access_to_cameras"],
        zone_ids=data["access_to_zones"]
    )
    if success:
        return redirect(url_for('users.user_manage'))
    return [{'message':message}]



@users_bp.route('/edit',  methods=['PATCH'])
@permission_required(['edit'])
@jwt_required()
def edit_user():
    schema = EditUserSchema()
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    print('data' , data)
    validated_data = schema.load(data)
    print('validated_data' , validated_data)
    
    camera_access = validated_data.get('camera_access', [])
    zone_access = validated_data.get('zone_access', [])
    user_access = validated_data.get('user_access', [])
    
    new_permission_names = camera_access + zone_access + user_access

    success, message, status = handle_edit_user(
        old_firstname=validated_data.get('old_firstname'),
        firstname=validated_data.get('firstname'),
        old_lastname=validated_data.get('old_lastname'),
        lastname=validated_data.get('lastname'),
        username=validated_data.get('old_username'),
        new_username=validated_data.get('new_username'),
        password=validated_data.get('old_password'),
        new_password=validated_data.get('new_password'),
        new_permission_names=new_permission_names,
        camera_ids=validated_data.get('access_to_cameras'),
        zone_ids=validated_data.get('access_to_zones'),
    )

    if success:
        return {"success": success, "message": message}, 200
    else:
        return {"success": success, "message": message }, 400


