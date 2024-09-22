from flask import redirect, url_for, render_template, request, flash
from flask_login import login_user, logout_user
import os
from flask_jwt_extended import jwt_required
from .controller import handle_login, handle_registration, handle_logout, handle_add_users, handle_delete_user, handle_edit_user, user_list
from src.users import users_bp
from .model import Accesses, Permissions, UserAccess, Module, Users
from src.permissions import permission_required


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
    return render_template('register.html')


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

            response.headers['Location'] = url_for('home_page')
            response.status_code = 302

            return response

        flash(message=message)
        return redirect(url_for('users.login'))
    return render_template('login.html')


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
    list_userss = Users.query.all()
    accesses = Accesses.query.join(Permissions).join(Module).all()
    return render_template('user-manage.html', users=list_userss, accesses=accesses)


@users_bp.route('/delete-users/<username>', methods=["DELETE"])
@permission_required(['delete'])
@jwt_required()
def delete_user(username):
    success, message, status = handle_delete_user(username)
    if success:
        return ({'success': True, 'message': message}), 200
    else:
        return ({'success': False, 'message': message}), status


@users_bp.route('/create', methods=["POST", 'GET'])
@permission_required(['create'])
@jwt_required()
def add_user():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        camera_access = request.form.getlist('camera_access')
        zone_access = request.form.getlist('zone_access')
        user_access = request.form.getlist('user_access')

        all_permissions = camera_access + zone_access + user_access

        success, message, status = handle_add_users(
            username, password, email, all_permissions)

        if success:
            return redirect(url_for('users.user_manage'))
        return redirect(url_for('users.add_user'))

    accesses = Accesses.query.join(Permissions).join(Module).all()
    return render_template('add-users.html', accesses=accesses)


@users_bp.route('/profile/<username>',  methods=['PUT'])
@permission_required(['edit'])
@jwt_required()
def edit_user(username):
    user_data = request.get_json()

    new_username = user_data.get('new_username')
    new_email = user_data.get('new_email')
    password = user_data.get('password')
    new_password = user_data.get('new_password')

    success, message, status_code = handle_edit_user(
        username, new_username, password, new_password, new_email)

    if success:
        flash(message, 'success')
        # return redirect(url_for('users.user_manage'))
        return {"message": message}, 200
    else:
        flash(message, 'error')
        return {'message': message}, 400
