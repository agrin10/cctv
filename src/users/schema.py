from marshmallow import Schema , fields , validate , ValidationError


class AddUserSchema(Schema):
    firstName = fields.Str(required=False , validate=validate.Length(min=2 , max=20))
    lastName = fields.Str(required=False , validate=validate.Length(min=2 , max=20))
    username = fields.Str(required=True , validate=validate.Length(min=3 , max=20))
    password = fields.Str(required=True , validate=validate.Length(min=3 , max=20))
    camera_access = fields.List(fields.String(), required=False, missing=[])  
    zone_access = fields.List(fields.String(), required=False, missing=[])  
    user_access = fields.List(fields.String(), required=False, missing=[])  
    access_to_cameras = fields.List(fields.String(), required=False, missing=[])  
    access_to_zones = fields.List(fields.String(), required=False, missing=[])  



    
class EditUserSchema(Schema):
    old_firstname = fields.Str(required=False , validate=validate.Length(min=2 , max=20))
    old_lastname = fields.Str(required=False , validate=validate.Length(min=2 , max=20))
    old_username = fields.Str(required=True , validate=validate.Length(min=2 , max=20))
    old_password = fields.Str(required=True )
    firstname = fields.Str(required=False , validate=validate.Length(min=2 , max=20))
    lastname = fields.Str(required=False , validate=validate.Length(min=2 , max=20))
    new_username = fields.Str(required=True , validate=validate.Length(min=3 , max=20))
    password = fields.Str(required=True , validate=validate.Length(min=3 , max=20))
    camera_access = fields.List(fields.String(), required=False, missing=[])  
    zone_access = fields.List(fields.String(), required=False, missing=[])  
    user_access = fields.List(fields.String(), required=False, missing=[])  
    access_to_cameras = fields.List(fields.String(), required=False, missing=[])  
    access_to_zones = fields.List(fields.String(), required=False, missing=[])  