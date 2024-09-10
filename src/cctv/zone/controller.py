from .model import Users , db
from src import login_manager
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, get_jwt_identity
from flask import jsonify , make_response
from datetime import timedelta
from pytz import timezone 



@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


def handle_registration(username , password , email):
    
    existing_user = Users.query.filter_by(username = username).first()
    existing_email = Users.query.filter_by(email = email).first()
    if existing_user:
        return False , 'username already exists' 
    if password is None:
        return False , 'password is required' 
    if existing_email:
        return False , 'email already exists'
    if len(password) < 8 :
        return False , 'Password must be at least 8 characters long'
    
    new_user = Users(username = username , email = email , password = password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return True , 'registration successful, please login'
    except Exception as e:
            db.session.rollback()
            return False, f'An error occurred: {str(e)}'         



# def handle_login(username, password):
#     user = Users.query.filter_by(username=username).first()
#     if not user:
#         response = make_response(jsonify({
#             "msg": "Invalid username or password"
#         }), 401)   
#         return None, False, 'Invalid username or password', response

#     if user.check_password(password):
#         access_token = create_access_token(identity=user.user_id)
#         refresh_token = create_refresh_token(identity=user.user_id, expires_delta=timedelta(days=1))
#         # print(f'access token {access_token}')
#         # print(f'refresh token {refresh_token}')
#         if access_token is None:
#             raise Exception("Access token not generated")
#         if refresh_token is None:
#             raise Exception("Refresh token not gen``erated")

#         response = make_response(jsonify({
#             "msg": "Login successful",
            
#         }))

#         # Set cookies securely
#         response.set_cookie('access_token_cookie', access_token, httponly=True, samesite='Strict')
#         set_refresh_cookies(response, refresh_token)
#         print(user)
#         return user, True, 'Login successful', response
#     else:
#         response = make_response(jsonify({
#             "msg": "Invalid username or password"
#         }), 401)  # Unauthorized status code
#         return None, False, 'Invalid username or password', response
    

def handle_login(username, password):
    user = Users.query.filter_by(username=username).first()
    if user and user.check_password(password) :
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
