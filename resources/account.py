from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required,get_jwt,get_jwt_identity
from flask import jsonify
from db import db
from models.account import AccountModel
from schemas import AccountSchema, AccountUpdateSchema
from resources.user import get_user_id

account_blp = Blueprint("accounts", "accounts", description="Operations on accounts", url_prefix="/accounts")

@account_blp.route('/')
class Accounts(MethodView):
    @jwt_required()
    @account_blp.response(200, AccountSchema(many=True))
    def get(self):
        user_id = get_user_id()

        return AccountModel.query.filter_by(user_id=user_id).all()

    @account_blp.arguments(AccountSchema)
    @jwt_required()
    @account_blp.response(200, AccountSchema)
    def post(self, account_data):
        user_id = get_user_id()
        new_account = AccountModel(user_id=user_id, account_type="savings", balance=0.0)

        db.session.add(new_account)
        db.session.commit()

        return new_account

@account_blp.route('/<int:account_id>')
class Account(MethodView):
    @jwt_required()
    @account_blp.response(200, AccountSchema)
    def get(self, account_id):
        user_id = get_user_id()
        account = AccountModel.query.filter_by(id=account_id, user_id=user_id).first()
        if not account:
            abort(403, message="You don't have permission")
        return account

    @account_blp.arguments(AccountUpdateSchema)
    @jwt_required()
    @account_blp.response(200, AccountSchema)
    def put(self, account_data, account_id):
        user_id = get_user_id()
        account = AccountModel.query.filter_by(id=account_id, user_id=user_id).first()
        if not account:
            abort(403, message="You don't have permission")

        if 'type' in account_data:
            account.type = account_data["type"]

        account.account_type = account_data["account_type"]
        account.balance = account_data["balance"]
        db.session.commit()

        return account

    @jwt_required()
    @account_blp.response(200, AccountSchema)
    def delete(self, account_id):
        user_id = get_user_id()
        account = AccountModel.query.filter_by(id=account_id, user_id=user_id).first()
        if not account:
            abort(403, message="Account not found")

        db.session.delete(account)
        db.session.commit()
        return jsonify({"message": "Account deleted successfully"}), 200
