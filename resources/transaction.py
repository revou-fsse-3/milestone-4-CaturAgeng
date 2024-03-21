from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models.transaction import TransactionModel  
from models.account import AccountModel
from schemas import TransactionSchema, TransactionUpdateSchema
from resources.user import get_user_id
from flask_jwt_extended import jwt_required
from flask import jsonify

transaction_blp = Blueprint("transactions", "transactions", description="Operations on transactions", url_prefix="/transactions")

@transaction_blp.route('/')
class Transactions(MethodView):
    @jwt_required()
    @transaction_blp.response(200, TransactionSchema(many=True))
    def get(self):
        user_id = get_user_id()
        account_id = (
            AccountModel.query.with_entities(AccountModel.id).filter_by(user_id=user_id).all()
        )
        if account_id:
            account_id_list = [account[0] for account in account_id]
            transaction_list =[]
            for account_id in account_id_list:
                transactions = TransactionModel.query.filter(
                    (TransactionModel.to_account_id == account_id) | (TransactionModel.from_account_id == account_id)
                ).all()
                transaction_list.extend(transactions)
            return transaction_list
        return jsonify({"meesage": "Transaction not foun!"}), 404

    @transaction_blp.arguments(TransactionUpdateSchema)
    @jwt_required()
    @transaction_blp.response(200, TransactionSchema)
    def post(self, transaction_data):
        try:
            user_id = get_user_id()
            if transaction_data["type"] == "deposit":
                to_account = AccountModel.query.filter_by(
                    id=user_id
                ).first()

                if to_account is None:
                    return jsonify({"message": "Account not found"}), 404
                
                new_transaction = TransactionModel(
                    from_account_id = None,
                    to_account_id = transaction_data["to_account_id"],
                    amount = transaction_data["amount"],
                    type = "deposit",
                    description = transaction_data["description"],
                )
                to_account.balance = getattr(to_account, "balance", 0) + transaction_data["amount"]
                db.session.add(new_transaction)
                db.session.commit()
                return jsonify({"message": "Deposit Successfuly!"}), 200
            
            elif transaction_data["type"] == "transfer":
                from_account = AccountModel.query.filter_by(
                    id=transaction_data["from_account_id"], user_id=user_id
                ).first()
                to_account = AccountModel.query.filter_by(
                    id=transaction_data["to_account_id"], user_id=user_id
                ).first()

                if from_account is None or to_account is None:
                    return jsonify({"message": "One or more accounts not found"}), 404

                if from_account.balance < transaction_data["amount"]:
                    return jsonify({"message": "Insufficient balance!"}), 400
                new_transaction = TransactionModel(
                    from_account_id = transaction_data["from_account_id"],
                    to_account_id = transaction_data["to_account_id"],
                    amount = transaction_data["amount"],
                    type = "transfer",
                    description = transaction_data["description"],
                )
                to_account.balance += transaction_data["amount"]
                from_account.balance -= transaction_data["amount"]
                db.session.add(new_transaction)
                db.session.commit()
                return jsonify({"message": "Transfer successfuly!"}), 200
            
            elif transaction_data["type"] == "withdrawal":
                from_account = AccountModel.query.filter_by(
                    id=transaction_data["from_account_id"], user_id=user_id
                ).first()

                if from_account.balance < transaction_data["amount"]:
                    return jsonify({"message": "Insufficient balance!"}), 400
                new_transaction = TransactionModel(
                    from_account_id = transaction_data["from_account_id"],
                    to_account_id = None,
                    amount = transaction_data["amount"],
                    type = "withdrawal",
                    description = transaction_data["description"],
                )
                from_account.balance -= transaction_data["amount"]
                db.session.add(new_transaction)
                db.session.commit()
                return jsonify({"message": "Withdrawal successfuly!"}), 200
            else:
                return jsonify({"Error": "Invalid transaction type!"}), 400
        except SQLAlchemyError:
            return jsonify({"Error": "Internal server error!"}), 500


@transaction_blp.route('/<int:transaction_id>')
class Transaction(MethodView):
    @jwt_required()
    @transaction_blp.response(200, TransactionSchema)
    def get(self, transaction_id):
        user_id = get_user_id()
        account_id = (
            AccountModel.query.with_entities(AccountModel.id).filter_by(user_id=user_id).all()
        )
        account_id_list = [account[0] for account in account_id]
        transaction = db.session.get(TransactionModel, transaction_id)
        if transaction is None:
            return jsonify({"Message": "Transaction not found!"}), 404
        if transaction and (
            transaction.from_account_id in account_id_list or transaction.to_account_id in account_id_list
        ):
            return transaction
        else: 
            return jsonify({"Message": "You doesn't have permission!"}), 403
        

