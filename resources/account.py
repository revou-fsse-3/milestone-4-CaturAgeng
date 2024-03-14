from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models.account import AccountModel
from schemas import AccountSchema

account_blp = Blueprint("accounts", "accounts", description="Operations on accounts", url_prefix="/accounts")

@account_blp.route('/')
class Accounts(MethodView):
    @account_blp.response(200, AccountSchema(many=True))
    def get(self, user_id):
        # Assuming you have some way to get the currently authenticated user
        # Replace the following line with your authentication logic
        # Example: user = get_current_authenticated_user()
        # user_id = 1  # Replace with the actual user ID
        return AccountModel.query.filter_by(user_id=user_id).all()

    @account_blp.arguments(AccountSchema)
    @account_blp.response(200, AccountSchema)
    def post(self, account_data, user_id):
        # Assuming you have some way to get the currently authenticated user
        # Replace the following line with your authentication logic
        # Example: user = get_current_authenticated_user()
        # user_id = 1  # Replace with the actual user ID

        account = AccountModel(user_id=user_id, **account_data)
        try:
            db.session.add(account)
            db.session.commit()
        except IntegrityError:
            abort(http_status_code=400, message="An account with that account number already exists.")
        except SQLAlchemyError:
            abort(http_status_code=500, message="An error occurred while inserting the account.")

        return account

@account_blp.route('/<int:account_id>')
class Account(MethodView):
    @account_blp.response(200, AccountSchema)
    def get(self, account_id):
        account = AccountModel.query.get_or_404(account_id)
        # Assuming you have some way to check authorization
        # Replace the following line with your authorization logic
        # Example: authorize_user(account.user_id)
        return account

    @account_blp.arguments(AccountSchema)
    @account_blp.response(200, AccountSchema)
    def put(self, account_data, account_id):
        account = AccountModel.query.get_or_404(account_id)
        # Assuming you have some way to check authorization
        # Replace the following line with your authorization logic
        # Example: authorize_user(account.user_id)

        AccountModel.query.filter_by(id=account_id).update(account_data)
        db.session.commit()
        return account

    @account_blp.response(200, AccountSchema)
    def delete(self, account_id):
        account = AccountModel.query.get_or_404(account_id)
        # Assuming you have some way to check authorization
        # Replace the following line with your authorization logic
        # Example: authorize_user(account.user_id)

        db.session.delete(account)
        db.session.commit()
        return {"message": "Account deleted"}
