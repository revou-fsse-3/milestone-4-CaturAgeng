# from flask_smorest import abort, Blueprint
# from flask.views import MethodView
# from sqlalchemy.exc import SQLAlchemyError, IntegrityError
# from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity, jwt_required
# from passlib.hash import pbkdf2_sha256
# from functools import wraps
# from sqlalchemy import select
# from db import db
# from models.user import UserModel  
# from schemas import UserSchema, PlainUserSchema

# auth_blp = Blueprint("auth", "auth", description="Operations on auth", url_prefix="/auth")

# @auth_blp.route("/register-jwt")
# class UserRegister(MethodView):
#     @auth_blp.arguments(PlainUserSchema)
#     @auth_blp.response(200, PlainUserSchema)
#     def post(self, user_data):
#         try:
#             user = UserModel(
#                 username=user_data["username"],
#                 password_hash=pbkdf2_sha256.hash(user_data["password_hash"]),
#                 role="user"
#             )
#             # db.session.add(user)
#             # db.session.commit()
#             # add_item di ambil dari file common
#             user.get_item()
#         except IntegrityError:
#             abort(400, message="A user with that username already exists.")
#         except SQLAlchemyError:
#             abort(500, message="An error occurred while adding the user.")

#         return user

# @auth_blp.route("/login-jwt")
# class UserLogin(MethodView):
#     @auth_blp.arguments(UserSchema)
#     def post(self, user_data):
#         user = db.session.execute(select(UserModel).where(UserModel.username == user_data["username"])).first()[0]
#         if user and pbkdf2_sha256.verify(user_data["password_hash"], user.password_hash):
#             access_token = create_access_token(identity={"id": user.id, "role": user.role}, fresh=True)
#             refresh_token = create_refresh_token(identity={"id": user.id, "role": user.role})
#             return {"access_token": access_token, "refresh_token": refresh_token}, 200

#         abort(401, message="Invalid credentials.")

# @auth_blp.route("/refresh-jwt")
# class TokenRefresh(MethodView):
#     @jwt_required(refresh=True)
#     def post(self):
#         current_user = get_jwt_identity()
#         new_token = create_access_token(identity=current_user, fresh=False)
#         return {"access_token": new_token}, 200

# def admin_required(role_required="admin"):
#     def decorator(func):
#         @wraps(func)
#         @jwt_required()
#         def wrapper(*args, **kwargs):
#             jwt = get_jwt()
#             if jwt.get("sub").get("role") != role_required:
#                 abort(401, message=f"{role_required.capitalize()} privilege required.")
#             return func(*args, **kwargs)

#         return wrapper

#     return decorator

# def get_user_id():
#     jwt = get_jwt()
#     return jwt.get("sub").get("id")
