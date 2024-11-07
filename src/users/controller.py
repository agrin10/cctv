from .model import Users , db , Permissions , Accesses , UserAccess , Module
from src import login_manager
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, get_jwt_identity
from flask import jsonify , make_response
from datetime import timedelta
from sqlalchemy.exc import SQLAlchemyError




def handle_registration(username, password, email):
    existing_user = Users.query.filter_by(username=username).first()
    existing_email = Users.query.filter_by(email=email).first()
    
    if existing_user:
        return False, 'Username already exists' 
    if password is None:
        return False, 'Password is required' 
    if existing_email:
        return False, 'Email already exists'
    if len(password) < 8:
        return False, 'Password must be at least 8 characters long'
    
    new_user = Users(username=username, email=email)
    new_user.set_password(password) 
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return True, 'Registration successful, please login'
    except Exception as e:
        db.session.rollback()
        return False, f'An error occurred: {str(e)}'



def handle_login(username, password):
    user = Users.query.filter_by(username=username).first()
    if user and user.check_password(password) :
        print('valid password')
        print("Hashed password:", user.password_hash)
        access_token = create_access_token(identity=user.user_id)
        refresh_token = create_refresh_token(identity=user.user_id, expires_delta=timedelta(days=1))
        
        response = make_response(jsonify({
            "msg": "Login successful"
        }))

        response.set_cookie('access_token_cookie', access_token, httponly=True, samesite='Strict')
        set_refresh_cookies(response, refresh_token)

        
        return user, True, 'Login successful', response 
    return None, False, 'Invalid username or password', None
    

def handle_refresh_token():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    resp = 'refresh : true'
    set_access_cookies(resp, access_token)
    return resp, 200
    
def handle_logout():
    response = make_response(jsonify({"msg": "Logout successful"}))
    response.delete_cookie('access_token_cookie')
    response.delete_cookie('refresh_token_cookie') 
    return response

def user_list():
    try:
        users = Users.query.all()
        list_users = []
        list_users=[Users.toDict(user) for user in users]
        return list_users
    except Exception as e:
        db.session.rollback()
        return False, f"An error occurred: {str(e)}"



def handle_add_users(firstname, lastname,username, password, permission_names):
    existing_user = Users.query.filter(Users.username == username).first()
    if existing_user:
        return False, 'Username or email already exists.', 400
    
    new_user = Users(name= firstname , last_name =lastname , username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    
    db.session.commit()

    for permission_name in permission_names:
        permission_obj = Permissions.query.filter_by(name=permission_name).first()
        if permission_obj:  
            access = Accesses.query.filter_by(permissions_id=permission_obj.id).first()
            
            if access:  
                module = Module.query.get(access.module_id)
                if module:  
                    user_access = UserAccess(user_id=new_user.user_id, access_id=access.id)
                    db.session.add(user_access)

    db.session.commit()

    return True, 'User added successfully with the specified accesses.', 200




def handle_edit_user(username, new_username, password, new_password, new_permission_names):
    user = Users.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        user.username = new_username
        if new_password:
            user.set_password(new_password)
        
        # Clear current permissions and accesses
        UserAccess.query.filter_by(user_id=user.user_id).delete()
        
        for permission_name in new_permission_names:
            permission_obj = Permissions.query.filter_by(name=permission_name).first()
            if permission_obj:
                access = Accesses.query.filter_by(permissions_id=permission_obj.id).first()
                
                if access:
                    module = Module.query.get(access.module_id)
                    if module:
                        user_access = UserAccess(user_id=user.user_id, access_id=access.id)
                        db.session.add(user_access)
        
        try:
            db.session.commit()
            return True, "User updated successfully with the specified accesses.", 200
        except Exception as e:
            db.session.rollback() 
            return False, f"Update failed: {e}", 400
    
    return False, 'User not found or password incorrect', 400

    
def handle_delete_user(username):
    user = Users.query.filter_by(username=username).first()
    try:
        db.session.delete(user)
        db.session.commit()
        return True , "user deleted successfully." , 200
    except Exception as e:
        db.session.rollback()
        return False , "delete faild" , 400
def get_permissions(permission_id):
    permissions = Permissions.query.filter_by(id=permission_id)
    response = []
    for permission in permissions:
        response.append(permission)
    return response

