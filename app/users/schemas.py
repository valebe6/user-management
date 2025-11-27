from marshmallow import Schema, fields, validate

class UserCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=80))
    email = fields.Email(required=True)
    age = fields.Int(required=False, validate=validate.Range(min=0, max=120))

class UserUpdateSchema(Schema):
    name = fields.Str(required=False, validate=validate.Length(min=2, max=80))
    email = fields.Email(required=False)
    age = fields.Int(required=False, validate=validate.Range(min=0, max=120))

class UserOutSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    email = fields.Email()
    age = fields.Int(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime(allow_none=True)
