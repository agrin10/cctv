from .model import Users , db , Permissions , Accesses , UserAccess , Module
from src import login_manager
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, get_jwt_identity
from flask import jsonify , make_response
from datetime import timedelta
from sqlalchemy.exc import SQLAlchemyError
from src.camera.model import Camera
from src.zone.model import Zone




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


def handle_add_users(firstname, lastname, username, password, permission_names, camera_ids, zone_ids):

    # Check if the username already exists
    existing_user = Users.query.filter(Users.username == username).first()
    if existing_user:
        return False, 'Username or email already exists.', 400

    new_user = Users(name=firstname, last_name=lastname, username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    for permission_name in permission_names:
        permission_obj = Permissions.query.filter_by(name=permission_name).first()
        if permission_obj:
            access = Accesses.query.filter_by(permissions_id=permission_obj.id).first()
            if access:
                user_access = UserAccess(user_id=new_user.user_id, access_id=access.id)
                db.session.add(user_access)

    if camera_ids:
        for camera_id in camera_ids:
            camera = Camera.query.get(camera_id)
            if camera:
                default_camera_permission = Permissions.query.filter_by(name="Camera Access").first()
                if not default_camera_permission:
                    default_camera_permission = Permissions(name="Camera Access")
                    db.session.add(default_camera_permission)
                    db.session.commit()

                camera_access = Accesses(camera_id=camera.camera_id, permissions_id=default_camera_permission.id)
                db.session.add(camera_access)
                db.session.commit()

                user_camera_access = UserAccess(user_id=new_user.user_id, access_id=camera_access.id)
                db.session.add(user_camera_access)

    if zone_ids:
        for zone_id in zone_ids:
            zone = Zone.query.get(zone_id)
            if zone:
                default_zone_permission = Permissions.query.filter_by(name="Zone Access").first()
                if not default_zone_permission:
                    default_zone_permission = Permissions(name="Zone Access")
                    db.session.add(default_zone_permission)
                    db.session.commit()

                zone_access = Accesses(zone_id=zone.zone_id, permissions_id=default_zone_permission.id)
                db.session.add(zone_access)
                db.session.commit()

                user_zone_access = UserAccess(user_id=new_user.user_id, access_id=zone_access.id)
                db.session.add(user_zone_access)

    db.session.commit()

    return True, 'User added successfully with the specified accesses.', 200



def handle_edit_user(
    old_firstname, firstname, old_lastname, lastname, 
    username, new_username, password, new_password, 
    new_permission_names, camera_ids, zone_ids
):
    user = Users.query.filter_by(username=username).first()

    if user:
        user.username = new_username
        user.name = firstname
        user.last_name = lastname
        if new_password:
            user.set_password(new_password)

        UserAccess.query.filter_by(user_id=user.user_id).delete()

        # Assign new permissions
        for permission_name in new_permission_names:
            permission_obj = Permissions.query.filter_by(name=permission_name).first()
            if permission_obj:
                access = Accesses.query.filter_by(permissions_id=permission_obj.id).first()
                if access:
                    user_access = UserAccess(user_id=user.user_id, access_id=access.id)
                    db.session.add(user_access)

        if camera_ids:
            for camera_id in camera_ids:
                camera = Camera.query.filter_by(camera_id=camera_id).first()
                if camera:
                    access = Accesses.query.filter_by(camera_id=camera.camera_id).first()
                    if access:
                        user_access = UserAccess(user_id=user.user_id, access_id=access.id)
                        db.session.add(user_access)

        if zone_ids:
            for zone_id in zone_ids:
                zone = Zone.query.filter_by(zone_id=zone_id).first()
                if zone:
                    access = Accesses.query.filter_by(zone_id=zone.zone_id).first()
                    if access:
                        user_access = UserAccess(user_id=user.user_id, access_id=access.id)
                        db.session.add(user_access)

        try:
            db.session.commit()
            return (True, "User updated successfully with the specified accesses.", 200)
        except Exception as e:
            db.session.rollback()
            return (False, f"Update failed: {e}", 400)

    return (False, 'User not found or password incorrect', 400)

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



def get_user_accesses(user_id):
    
    user = Users.query.filter_by(user_id=user_id).first()

    if not user:
        return {"error": "User not found"}

    result = {
        "user_id": user.user_id,
        "username": user.username,
        "permissions": [],
        "cameras": [],
        "zones": []
    }

    for user_access in user.user_accesses:
        access = user_access.access
        if access.permission:
            result["permissions"].append({
                "permission_id": access.permissions_id,
                "permission_name": access.permission.name,
                "permission_label": access.permission.label
            })
        if access.camera:
            result["cameras"].append({
                "camera_id": access.camera.camera_id,
                "camera_name": access.camera.camera_name
            })
        if access.zone:
            result["zones"].append({
                "zone_id": access.zone.zone_id,
                "zone_name": access.zone.zone_name
            })

    return result
