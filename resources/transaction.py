from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models.transaction import TransactionModel  
from schemas import TransactionSchema  
from resources.user import get_user_id
from flask_jwt_extended import jwt_required

transaction_blp = Blueprint("transactions", "transactions", description="Operations on transactions", url_prefix="/transactions")

@transaction_blp.route('/')
class Transactions(MethodView):
    @jwt_required()
    @transaction_blp.response(200, TransactionSchema(many=True))
    def get(self):
        user_id = get_user_id()
        return TransactionModel.query.filter_by().all()

    @transaction_blp.arguments(TransactionSchema)
    @jwt_required()
    @transaction_blp.response(200, TransactionSchema)
    def post(self, transaction_data):
        user_id = get_user_id()

        # Set the user_id in the transaction data
        transaction_data["from_account_id"] = user_id

        transaction = TransactionModel(**transaction_data)
        try:
            db.session.add(transaction)
            db.session.commit()
        except IntegrityError:
            abort(http_status_code=400, message="An error occurred while creating the transaction.")
        except SQLAlchemyError:
            abort(http_status_code=500, message="An error occurred while inserting the transaction.")

        return transaction

@transaction_blp.route('/<int:transaction_id>')
class Transaction(MethodView):
    @jwt_required()
    @transaction_blp.response(200, TransactionSchema)
    def get(self, transaction_id):
        user_id = get_user_id()
        transaction = TransactionModel.query.filter_by(user_id)
        
        return transaction
