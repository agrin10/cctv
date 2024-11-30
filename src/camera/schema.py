from marshmallow import fields , validate , ValidationError , Schema

class AddCameraSchema(Schema):
    ipAddress = fields.Str(
        required=True,
        validate=validate.Regexp(
            r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$",
            error="Invalid IP address format",
        ),
    )
    deviceName = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    camera_username = fields.Str(required=True, validate=validate.Length(min=3))
    camera_password = fields.Str(required=True, validate=validate.Length(min=6))
    deviceType = fields.Str(required=True, validate=validate.Length(min=0))
    zone_name = fields.Str(required=True, validate=validate.Length(min=3))
    is_record = fields.Bool(required=True)
    ai_properties = fields.List(fields.String(), required=False, missing=[])  

class EditCameraSchema(Schema):
    oldIpAddress = fields.Str(
        required=True,
        validate=validate.Regexp(
            r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$",
            error="Invalid IP address format",
        ),
    )
    newIpAddress = fields.Str(
        required=False,
        validate=validate.Regexp(
            r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$",
            error="Invalid IP address format",
        ),
    )
    deviceName = fields.Str(validate=validate.Length(min=0, max=50))
    camera_username = fields.Str(validate=validate.Length(min=3))
    camera_password = fields.Str(validate=validate.Length(min=6))
    deviceType = fields.Str(required=True, validate=validate.Length(min=0))
    camera_zones = fields.Str( required=True , validate=validate.Length(min=0))
    recording = fields.Str(
        validate=validate.OneOf(["yes", "no"], error="Recording must be 'yes' or 'no'")
    )
    ai_properties = fields.List(fields.String(), required=False) 
