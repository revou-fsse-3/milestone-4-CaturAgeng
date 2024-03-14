# schemas.py
from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(max=255))
    email = fields.Email(required=True, validate=validate.Length(max=255))
    password_hash = fields.Str(required=True, load_only=True, validate=validate.Length(max=255))
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)

    # Additional fields for User Management
    token = fields.Str(dump_only=True)

    class Meta:
        # Specify additional options if needed
        pass

class AccountSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    account_type = fields.String(required=True, validate=validate.Length(max=255))
    account_number = fields.String(required=True, validate=validate.Length(max=255))
    balance = fields.Decimal(required=True, places=2)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)

    class Meta:
        # Specify additional options if needed
        pass

class TransactionSchema(Schema):
    id = fields.Integer(dump_only=True)
    from_account_id = fields.Integer(required=False)
    to_account_id = fields.Integer(required=False)
    amount = fields.Decimal(required=True, places=2)
    type = fields.String(required=True, validate=validate.Length(max=255))
    description = fields.String(validate=validate.Length(max=255))
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        # Specify additional options if needed
        pass

class UserSchema(Schema):
    username = fields.String(required=True)
    email = fields.Email(required=True)

class PlainUserSchema(Schema):
    username = fields.String(required=True)