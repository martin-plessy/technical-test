from flask.testing import FlaskClient
from app.db import DatabaseConnection
from app.main import app as flask_app
from datetime import date, timedelta
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

@fixture
def arrange(client: FlaskClient):
    return Arrange(client)

TODAY = date.today()
TOMORROW = TODAY + timedelta(days=1)
OVERMORROW = TODAY + timedelta(days=2)

class Arrange:
    def __init__(self, client: FlaskClient):
        self._client = client

    def appointment(self, pet: int, employee: int, timeslot: int, date: date = TOMORROW):
        """
        Books an appointment for the date of tomorrow.
        """

        response = self._client.post('/api/v1.0/appointments/', json = {
            'pet': pet,
            'employee': employee,
            'timeslot': timeslot,
            'date': f'{date}'
        })

        assert response.status_code == 201

        return response
