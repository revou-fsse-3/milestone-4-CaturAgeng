import os
from flask import Flask
from flask_smorest import Api
from dotenv import load_dotenv
from db import db
from resources.user import user_blp as user_blueprint
from resources.account import account_blp as account_blueprint
from resources.transaction import transaction_blp as transaction_blueprint
from resources.auth import auth_blp

def create_app(is_test_env=False):
    app = Flask(__name__)
    load_dotenv()

    # Konfigurasi OpenAPI
    app.config["API_TITLE"] = "Book Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    # Konfigurasi Database
    if is_test_env is True:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///data.db")

    db.init_app(app)
    register_blueprints(app)
    with app.app_context():
        db.create_all()

    return app

def register_blueprints(app):
    api = Api(app)
    api.register_blueprint(user_blueprint)
    api.register_blueprint(account_blueprint)
    api.register_blueprint(transaction_blueprint)
    api.register_blueprint(auth_blp)

if __name__ == "__main__":
    app = create_app()
    app.run()
