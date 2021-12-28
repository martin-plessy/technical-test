from flask.testing import FlaskClient
from werkzeug import test

def test_empty(client: FlaskClient):
    response = client.get('/appointments/')

    assert response.status_code == 404
