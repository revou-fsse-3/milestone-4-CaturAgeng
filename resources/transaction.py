from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models.transaction import TransactionModel  # Import TransactionModel
from schemas import TransactionSchema  # Import TransactionSchema

transaction_blp = Blueprint("transactions", "transactions", description="Operations on transactions", url_prefix="/transactions")

@transaction_blp.route('/')
class Transactions(MethodView):
    @transaction_blp.response(200, TransactionSchema(many=True))
    def get(self, user_id):
        return TransactionModel.query.filter(
            (TransactionModel.from_account_id == user_id) | (TransactionModel.to_account_id == user_id)
        ).all()

    @transaction_blp.arguments(TransactionSchema)
    @transaction_blp.response(200, TransactionSchema)
    def post(self, transaction_data, user_id):

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
    @transaction_blp.response(200, TransactionSchema)
    def get(self, transaction_id):
        transaction = TransactionModel.query.get_or_404(transaction_id)
        
        return transaction
