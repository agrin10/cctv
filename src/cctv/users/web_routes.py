from flask import redirect , url_for , render_template , request , flash 
from flask_login import login_user , logout_user
import os
from flask_jwt_extended import  jwt_required  
from .controller import handle_login , handle_registration , handle_logout
from src.cctv.users import users_bp



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
        #TODO user is not identfy
        user, success, message, response = handle_login(username, password)
        print(user)

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
    
    response.headers['Location'] = url_for('login')  
    response.status_code = 302  
    return response
