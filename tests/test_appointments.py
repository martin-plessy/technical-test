from flask.testing import FlaskClient
from pytest import mark
from re import match
from tests.conftest import OVERMORROW, TODAY, TOMORROW, Arrange
from time import sleep
from typing import Any, Dict, Mapping

# Booking Appointments
# -----------------------------------------------------------------------------

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
    # Cancelled appointments don't cause conflicts.
    arrange.cancelled_appointment(pet=2, employee=3, timeslot=2) # Pet has appointment in the same practice.
    arrange.cancelled_appointment(pet=2, employee=1, timeslot=2) # Pet has appointment in another practice.
    arrange.cancelled_appointment(pet=3, employee=1, timeslot=2) # Owner has appointment in another practice.
    arrange.cancelled_appointment(pet=1, employee=2, timeslot=2) # Employee has appointment.
    arrange.cancelled_appointment(pet=2, employee=2, timeslot=2) # Double click.

    arrange.appointment(**arrange_data)

    response = client.post('/api/v1.0/appointments/', json = {
        'pet': 2,
        'employee': 2,
        'timeslot': 2,
        'date': f'{TOMORROW}',
    })

    assert response.status_code == 201
    assert response.mimetype == 'application/json'
    assert response.json['uid'] == 7

# Getting Appointments by UID
# -----------------------------------------------------------------------------

def test_get_invalid_mistyped_id(client: FlaskClient):
    assert client.get('/api/v1.0/appointments/frog').status_code == 404

def test_get_invalid_non_existent(client: FlaskClient):
    assert client.get('/api/v1.0/appointments/404').status_code == 404

def test_get_valid(client: FlaskClient, arrange: Arrange):
    created_uid = arrange.appointment(pet=1, employee=1, timeslot=1, date=TOMORROW).json['uid']

    response = client.get(f'/api/v1.0/appointments/{created_uid}')

    assert response.status_code == 200
    assert response.mimetype == 'application/json'
    assert response.json == {
        'uid': 1,
        'date': f'{TOMORROW}',
        'timeslot': {
            'start': '09:00:00',
            'end': '09:30:00',
        },
        'employee': {
            'uid': 1,
            'name': 'Carl Smith',
            'employee_type': {
                'uid': 1,
                'type': 'Veterinarian',
            },
        },
        'practice': {
            'uid': 1,
            'name': 'Plymouth Vets',
            'telephone': '01 752 000001',
            'address': '123 Test Street, Plymouth, Devon, PL1 1AA',
        },
        'pet': {
            'uid': 1,
            'name': 'Rex',
            'animal': 'Dog',
            'breed': 'Bonkus',
            'date_of_birth': '2019-12-24',
        },
        'owner': {
            'uid': 1,
            'name': 'Timmy Jerico',
            'telephone': '07 465 000001',
        },
        'is_cancelled': False,
        'cancellation_reason': None,
        'cancellation_time': None,
    }

# Cancelling Appointments by UID
# -----------------------------------------------------------------------------

def test_delete_invalid_mistyped_id(client: FlaskClient):
    assert client.delete('/api/v1.0/appointments/frog', json = {}).status_code == 404

def test_delete_invalid_non_existent(client: FlaskClient):
    assert client.delete('/api/v1.0/appointments/404', json = {}).status_code == 404

def test_delete_invalid_mistyped_reason(client: FlaskClient, arrange: Arrange):
    created_uid = arrange.appointment(pet=1, employee=1, timeslot=1).json['uid']

    response = client.delete(f'/api/v1.0/appointments/{created_uid}', json = {
        'reason': 42
    })

    assert response.status_code == 400
    assert response.mimetype == 'application/json'
    assert response.json['errors']['reason'] == '42 is not of type \'string\''

@mark.parametrize(('input', 'expected_reason'), [
    ({ }, 'No reason was provided for this cancellation.'),
    ({ 'reason': 'Cancelled for testing purposes.' }, 'Cancelled for testing purposes.'),
])
def test_delete_valid(client: FlaskClient, arrange: Arrange, input: Dict[str, Any], expected_reason: str):
    created_uid = arrange.appointment(pet=1, employee=1, timeslot=1).json['uid']

    response = client.delete(f'/api/v1.0/appointments/{created_uid}', json = input)

    assert response.status_code == 204
    assert response.data == b''

    response = client.get(f'/api/v1.0/appointments/{created_uid}')

    assert response.status_code == 200
    assert response.mimetype == 'application/json'
    assert response.json['is_cancelled'] == True
    assert response.json['cancellation_reason'] == expected_reason
    assert match('^2[01]\\d{2}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}$', response.json['cancellation_time']) is not None

def test_delete_valid_duplicate_update_reason_but_not_time(client: FlaskClient, arrange: Arrange):
    created_uid = arrange.appointment(pet=1, employee=1, timeslot=1).json['uid']

    client.delete(f'/api/v1.0/appointments/{created_uid}', json = {
        'reason': 'A'
    })

    response = client.get(f'/api/v1.0/appointments/{created_uid}')

    assert response.json['cancellation_reason'] == 'A'

    cancellation_time = response.json['cancellation_time']

    sleep(1)

    client.delete(f'/api/v1.0/appointments/{created_uid}', json = {
        'reason': 'B'
    })

    response = client.get(f'/api/v1.0/appointments/{created_uid}')

    assert response.json['cancellation_reason'] == 'B'
    assert response.json['cancellation_time'] == cancellation_time
