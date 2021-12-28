from app.db import DatabaseConnection
from app.main import app as flask_app
from flask.app import Flask
from pytest import fixture

@fixture
def app():
    with flask_app.app_context():
        DatabaseConnection()._reset_database()

    yield flask_app

@fixture
def client(app: Flask):
    return app.test_client()
