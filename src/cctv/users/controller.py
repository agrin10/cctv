from .model import Users , db , Permissions , Accesses , UserAccess , Module
from src import login_manager
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, get_jwt_identity
from flask import jsonify , make_response
from datetime import timedelta
from sqlalchemyseeder import ResolvingSeeder






def seed_user_mangement():
    session = db.session
    seeder = ResolvingSeeder(session)
    seeder.register(Accesses )
    seeder.register(Permissions )
    seeder.register(Module )
    seeder.register(UserAccess )
    seeder.register(Users)
    user_manage_path = "src/static/user-management.json"
    try:
        # Load new properties from the JSON file with UTF-8 encoding
        new_entities = seeder.load_entities_from_json_file(user_manage_path)
        for entity in new_entities:
            # Check if the entity already exists
            if isinstance(entity, Accesses):
                existing_access = session.query(Accesses).filter_by(permission_id=entity.permission_id).first()
                if existing_access:
                    print(f"Access with permission_id {entity.permission_id} already exists.")
                else:
                    session.add(entity)
                    print(f"Added new Access with permission_id {entity.permission_id}.")

            elif isinstance(entity, Permissions):
                existing_permission = session.query(Permissions).filter_by(name=entity.name).first()
                if existing_permission:
                    print(f"Permission with name {entity.name} already exists.")
                else:
                    session.add(entity)
                    print(f"Added new Permission with name {entity.name}.")

            elif isinstance(entity, Module):
                existing_module = session.query(Module).filter_by(name=entity.name).first()
                if existing_module:
                    print(f"Module with name {entity.name} already exists.")
                else:
                    session.add(entity)
                    print(f"Added new Module with name {entity.name}.")

        # Commit the session
        session.commit()
        print("Entities successfully committed to the database.")
    
    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
    
    finally:
        db.session.close()




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


def handle_add_user(username , password , email):
    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        return False , "user already exist." , 400
    new_user=Users(
        username=username,
        email=email
    )
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return True ,"user added successfully." , 200
    except Exception as e:
        db.session.rollback()
        return False , f'unsuccessfull :{e}', 400

def handle_edit_user(username , new_username , password , new_password ,new_email):
    user = Users.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        user.username = new_username
        user.email = new_email
        if new_password:
            user.set_password(new_password)

        try:
            db.session.commit()
            return True ,"user updated successfully." , 200
        except Exception as e:
            return False , f"update faild: {e}" , 400
    return False , 'user not found' , 400

    
def handle_delete_user(username):
    user = Users.query.filter_by(username=username).first()
    try:
        db.session.delete(user)
        db.session.commit()
        return True , "user deleted successfully." , 200
    except Exception as e:
        db.session.rollback()
        return False , "delete faild" , 400
    