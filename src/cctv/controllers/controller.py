from src.cctv.models.model import Users, db , Zone , Camera
from src import login_manager

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
    if len(password) > 8 :
        return False , 'Password must be at least 8 characters long'
    
    new_user = Users(username = username , email = email)
    new_user.set_password(password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return True , 'registration successful, please login'
    except Exception as e:
            db.session.rollback()
            return False, f'An error occurred: {str(e)}'         
        

def handle_login(username , password):
    user = Users.query.filter_by(username = username).first()
    if user is None:
        return user , False , 'username not found' 
    if user.check_password(password):
        return user ,  True , 'login successfully' 
    return user,  False,'invalid password' 

def user_list():
    try:
        users = Users.query.all()
        list_users = []
        list_users=[Users.toDict(user) for user in users]
        return list_users
    except Exception as e:
        db.session.rollback()
        return False, f"An error occurred: {str(e)}"

def handle_add_zone(zone_name , zone_desc):
    existing_zone = Zone.query.filter_by(zone_name = zone_name).first()
    if existing_zone:
        return False , "entered location already exists"
    new_zone = Zone(zone_name = zone_name , zone_desc = zone_desc)
    db.session.add(new_zone)
    db.session.commit()
    return True , 'zone added successfully'

    
def handle_retrieves_zone():
    try:
        zones = Zone.query.all()
        zones = [Zone.toDict(zones) for zones in zones]
        return zones
    except Exception as e:
        db.session.rollback()
        return False, f'An error occurred: {str(e)}'
    

def handle_add_camera(camera_ip, camera_name, camera_username, camera_type, camera_password, zone_name):
    existing_camera = Camera.query.filter_by(camera_ip=camera_ip).first()
    if existing_camera:
        return False, "Camera already exists."

    zone = Zone.query.filter_by(zone_name=zone_name).first()
    if zone is None:
        return False, f"Zone '{zone_name}' not found."

    new_camera = Camera(
        camera_ip=camera_ip,
        camera_name=camera_name,
        camera_username=camera_username,
        camera_type=camera_type,
        camera_zone=zone_name
    )
    new_camera.set_password(camera_password)

    try:
        db.session.add(new_camera)
        db.session.commit()
        return True, "Camera added successfully."
    except Exception as e:
        db.session.rollback()
        return False, f"An error occurred: {str(e)}"



def handle_retrieves_camera():
    try:
        cameras = Camera.query.all()
        cameras = [Camera.toDict(camera) for camera in cameras]
        return cameras
    except Exception as e:
        db.session.rollback()
        return False, f'An error occurred: {str(e)}'