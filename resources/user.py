from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models.user import UserModel
from schemas import UserSchema
from flask_jwt_extended import jwt_required

user_blp = Blueprint("users", "users", description="Operations on users", url_prefix="/users")

@user_blp.route('/')
class Users(MethodView):
    @user_blp.response(200, UserSchema(many=True))
    @jwt_required()
    def get(self):
        return UserModel.get_item()

    @user_blp.arguments(UserSchema)
    @user_blp.response(200, UserSchema)
    # @jwt_required()
    def post(self, user_data):
        user = UserModel(**user_data, role="user")
        try:
            # db.session.add(user)
            # db.session.commit()
            user.get_item()
        except IntegrityError:
            abort(http_status_code=400, message="A user with that username or email already exists.")
        except SQLAlchemyError:
            abort(http_status_code=500, message="An error occurred while inserting the user.")

        return user

@user_blp.route('/me')
class UserProfile(MethodView):
    @user_blp.response(200, UserSchema)
    def get(self):
        user = UserModel.query.get_or_404(1)
        return user

    @user_blp.arguments(UserSchema)
    @user_blp.response(200, UserSchema)
    def put(self, user_data):
        user = UserModel.query.get_or_404(1)

        UserModel.query.filter_by(id=user.id).update(user_data)
        db.session.commit()
        return user
