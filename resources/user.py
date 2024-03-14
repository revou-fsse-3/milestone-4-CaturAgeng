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
        return UserModel.query.all()

    @user_blp.arguments(UserSchema)
    @user_blp.response(200, UserSchema)
    def post(self, user_data):
        user = UserModel(**user_data)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(http_status_code=400, message="A user with that username or email already exists.")
        except SQLAlchemyError:
            abort(http_status_code=500, message="An error occurred while inserting the user.")

        return user

@user_blp.route('/me')
class UserProfile(MethodView):
    @user_blp.response(200, UserSchema)
    def get(self, user_id):
        # Assuming you have some way to get the currently authenticated user
        # Replace the following line with your authentication logic
        # Example: user = get_current_authenticated_user()
        user = UserModel.query.get_or_404(user_id)  # Replace with the actual user ID
        return user

    @user_blp.arguments(UserSchema)
    @user_blp.response(200, UserSchema)
    def put(self, user_data, user_id):
        # Assuming you have some way to get the currently authenticated user
        # Replace the following line with your authentication logic
        # Example: user = get_current_authenticated_user()
        user = UserModel.query.get_or_404(user_id)  # Replace with the actual user ID

        UserModel.query.filter_by(id=user.id).update(user_data)
        db.session.commit()
        return user
