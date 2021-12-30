from typing import Any, Mapping
from flask.testing import FlaskClient
from pytest import mark
from tests.conftest import OVERMORROW, TODAY, TOMORROW, Arrange

def test_post_valid(client: FlaskClient):
    response = client.post('/api/v1.0/appointments/', json = {
        'pet': 1,
        'employee': 1,
        'timeslot': 1,
        'date': f'{TOMORROW}',
    })

    assert response.status_code == 201
    assert response.mimetype == 'application/json'
    assert response.json['uid'] == 1

def test_post_invalid_missing_fields(client: FlaskClient):
    response = client.post('/api/v1.0/appointments/', json = {
    })

    assert response.status_code == 400
    assert response.mimetype == 'application/json'
    assert response.json['errors']['pet'] == '\'pet\' is a required property'
    assert response.json['errors']['employee'] == '\'employee\' is a required property'
    assert response.json['errors']['timeslot'] == '\'timeslot\' is a required property'
    assert response.json['errors']['date'] == '\'date\' is a required property'

def test_post_invalid_null_fields(client: FlaskClient):
    response = client.post('/api/v1.0/appointments/', json = {
        'pet': None,
        'employee': None,
        'timeslot': None,
        'date': None,
    })

    assert response.status_code == 400
    assert response.mimetype == 'application/json'
    assert response.json['errors']['pet'] == 'None is not of type \'integer\''
    assert response.json['errors']['employee'] == 'None is not of type \'integer\''
    assert response.json['errors']['timeslot'] == 'None is not of type \'integer\''
    assert response.json['errors']['date'] == 'None is not a \'date\''

def test_post_invalid_mistyped_fields(client: FlaskClient):
    response = client.post('/api/v1.0/appointments/', json = {
        'pet': 'frog',
        'employee': 'frog',
        'timeslot': 'frog',
        'date': 'frog',
    })

    assert response.status_code == 400
    assert response.mimetype == 'application/json'
    assert response.json['errors']['pet'] == '\'frog\' is not of type \'integer\''
    assert response.json['errors']['employee'] == '\'frog\' is not of type \'integer\''
    assert response.json['errors']['timeslot'] == '\'frog\' is not of type \'integer\''
    assert response.json['errors']['date'] == '\'frog\' is not a \'date\''

def test_post_invalid_wrong_valued_fields(client: FlaskClient):
    response = client.post('/api/v1.0/appointments/', json = {
        'pet': 404,
        'employee': 404,
        'timeslot': 404,
        'date': '1955-11-05',
    })

    assert response.status_code == 400
    assert response.mimetype == 'application/json'
    assert response.json['errors']['pet'] == '404 does not reference an existing entity'
    assert response.json['errors']['employee'] == '404 does not reference an existing entity'
    assert response.json['errors']['timeslot'] == '404 does not reference an existing entity'
    assert response.json['errors']['date'] == '\'1955-11-05\' cannot be a date in the past'

def test_post_invalid_past_timeslot_on_today_s_date(client: FlaskClient):
    response = client.post('/api/v1.0/appointments/', json = {
        'pet': 1,
        'employee': 1,
        'timeslot': 17, # A time slot that should always be in the past.
        'date': f'{TODAY}',
    })

    assert response.status_code == 400
    assert response.mimetype == 'application/json'
    assert response.json['errors']['timeslot'] == 'Value cannot be a timeslot in the past'

def test_post_conflict_pet_has_appointment_in_the_same_practice(client: FlaskClient, arrange: Arrange):
    arrange.appointment(pet=1, employee=2, timeslot=1)

    response = client.post('/api/v1.0/appointments/', json = {
        'pet': 1, # Same pet,
        'employee': 3, # Employees #2 and #3 both work in practice #2,
        'timeslot': 1, # Same time slot.
        'date': f'{TOMORROW}',
    })

    assert response.status_code == 409
    assert response.mimetype == 'application/json'
    assert response.json['message'] == 'The pet is already booked.'

def test_post_conflict_pet_has_appointment_in_another_practice(client: FlaskClient, arrange: Arrange):
    arrange.appointment(pet=1, employee=1, timeslot=1)

    response = client.post('/api/v1.0/appointments/', json = {
        'pet': 1, # Same pet,
        'employee': 2, # Employees #1 and #2 work in different practices,
        'timeslot': 1, # Same time slot.
        'date': f'{TOMORROW}',
    })

    assert response.status_code == 409
    assert response.mimetype == 'application/json'
    assert response.json['message'] == 'The pet is already booked.'

def test_post_conflict_owner_has_appointment_in_another_practice(client: FlaskClient, arrange: Arrange):
    arrange.appointment(pet=2, employee=1, timeslot=1)

    response = client.post('/api/v1.0/appointments/', json = {
        'pet': 3, # Pets #2 and #3 both have the same owner,
        'employee': 2, # Employees #1 and #2 work in different practices,
        'timeslot': 1, # Same time slot.
        'date': f'{TOMORROW}',
    })

    assert response.status_code == 409
    assert response.mimetype == 'application/json'
    assert response.json['message'] == 'Another pet is already booked.'

def test_post_valid_owner_has_appointment_in_the_same_practice(client: FlaskClient, arrange: Arrange):
    arrange.appointment(pet=2, employee=2, timeslot=1)

    response = client.post('/api/v1.0/appointments/', json = {
        'pet': 3, # Pets #2 and #3 both have the same owner,
        'employee': 3, # Employees #2 and #3 work in the same practice,
        'timeslot': 1, # Same time slot.
        'date': f'{TOMORROW}',
    })

    assert response.status_code == 201
    assert response.mimetype == 'application/json'
    assert response.json['uid'] == 2

def test_post_conflict_employee_has_appointment(client: FlaskClient, arrange: Arrange):
    arrange.appointment(pet=1, employee=1, timeslot=1)

    response = client.post('/api/v1.0/appointments/', json = {
        'pet': 2, # Pets #2 and #3 are unrealated,
        'employee': 1, # Same employee,
        'timeslot': 1, # Same time slot.
        'date': f'{TOMORROW}',
    })

    assert response.status_code == 409
    assert response.mimetype == 'application/json'
    assert response.json['message'] == 'Employee is already booked.'

def test_post_conflict_double_click(client: FlaskClient, arrange: Arrange):
    arrange.appointment(pet=1, employee=1, timeslot=1)

    response = client.post('/api/v1.0/appointments/', json = {
        'pet': 1, # Same pet,
        'employee': 1, # Same employee,
        'timeslot': 1, # Same time slot.
        'date': f'{TOMORROW}',
    })

    assert response.status_code == 409
    assert response.mimetype == 'application/json'
    assert response.json['message'] == 'The pet is already booked.'

@mark.parametrize('arrange_data', [
    dict(pet=2, employee=3, timeslot=2, date=OVERMORROW), # The pet is booked at this time, but another day, in the same practice.
    dict(pet=2, employee=1, timeslot=2, date=OVERMORROW), # The pet is booked at this time, but another day, in another practice.
    dict(pet=2, employee=3, timeslot=3, date=TOMORROW), # The pet is booked at this day, but another time, in the same practice.
    dict(pet=2, employee=1, timeslot=3, date=TOMORROW), # The pet is booked at this day, but another time, in another practice.
    dict(pet=3, employee=3, timeslot=2, date=OVERMORROW), # Another pet is booked at this time, but another day, in the same practice.
    dict(pet=3, employee=1, timeslot=2, date=OVERMORROW), # Another pet is booked at this time, but another day, in another practice.
    dict(pet=3, employee=3, timeslot=3, date=TOMORROW), # Another pet is booked at this day, but another time, in the same practice.
    dict(pet=3, employee=1, timeslot=3, date=TOMORROW), # Another pet is booked at this day, but another time, in another practice.
    dict(pet=1, employee=2, timeslot=2, date=OVERMORROW), # The employee is booked at this time, but another day.
    dict(pet=1, employee=2, timeslot=3, date=TOMORROW), # The employee is booked at this day, but another time.
])
def test_post_valid_amidst_other_appointments(client: FlaskClient, arrange: Arrange, arrange_data: Mapping[str, Any]):
    arrange.appointment(**arrange_data)

    response = client.post('/api/v1.0/appointments/', json = {
        'pet': 2,
        'employee': 2,
        'timeslot': 2,
        'date': f'{TOMORROW}',
    })

    assert response.status_code == 201
    assert response.mimetype == 'application/json'
    assert response.json['uid'] == 2
