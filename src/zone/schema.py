from marshmallow import Schema , fields ,   validate , ValidationError

class AddZoneSchema(Schema):
    zone_name = fields.Str(required=True , validate=validate.Length(min=3 , max=30))
    zone_desc = fields.Str(required=False , validate=validate.Length(min=2 , max=100))
