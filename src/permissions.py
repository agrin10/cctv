from functools import wraps
from flask import abort
from src.users.model import UserAccess , Accesses , Permissions
from flask_login import current_user

def get_current_user_id():
    if current_user.is_authenticated:
        return current_user.get_id()
    return None

def permission_required(permissions_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user_id = get_current_user_id()
            if not current_user_id or not user_has_permission(current_user_id , permissions_name):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator



def user_has_permission(user_id, permission_names):
    user_accesses = UserAccess.query.filter_by(user_id=user_id).all()
    
    user_permissions = set()  # Use a set for faster lookup
    for user_access in user_accesses:
        access = Accesses.query.get(user_access.access_id)
        if access:
            permission = Permissions.query.get(access.permissions_id)
            if permission:
                user_permissions.add(permission.name)

    # Check if any of the required permissions are in the user's permissions
    return any(permission in user_permissions for permission in permission_names)
