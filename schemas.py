from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str()
    password = fields.Str(required=True)

class UserUpdateSchema(Schema):
    username = fields.Str()
    password = fields.Str()
    email = fields.Str()
   
class AccountSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    account_type = fields.Str()
    account_number = fields.Str()
    balance = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    
class AccountUpdateSchema(Schema):
    user_id = fields.Int()
    account_type = fields.Str()
    account_number = fields.Str()
    balance = fields.Int()
    
class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    from_account_id = fields.Int()
    to_account_id = fields.Int()
    amount = fields.Int(required=True)
    type = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    

class TransactionUpdateSchema(Schema):
    from_account_id = fields.Int()
    to_account_id = fields.Int()
    amount = fields.Int()
    type = fields.Str()
    description = fields.Str()