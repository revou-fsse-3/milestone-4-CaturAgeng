import pytest
from app import create_app
from db import db

@pytest.fixture(autouse=True)
def test_app():
    app = create_app(is_test_env=True)
    app.config['TESTING'] = True
    yield app

    with app.app_context():
        db.drop_all()

# @pytest.fixture(autouse=True)
# def run_around_tests(test_app):
#     # Code that will run before test
#     yield
#     # code will run after test
#     with test_app.app_context():
#         db.drop_all()