from marshmallow import Schema ,fields , validate , ValidationError

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
    deviceType = fields.Str(required=True, validate=validate.Length(min=3))
    zone_name = fields.Str(required=True, validate=validate.Length(min=3))
    is_record = fields.Bool(required=True)
    ai_properties = fields.List(fields.String(), required=False, missing=[])  

