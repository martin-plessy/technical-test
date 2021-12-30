from app.Appointments.appointments_resources import AppointmentResources
from app.main import api
from datetime import date, datetime
from flask_restplus import abort, fields, Resource, marshal

ns = api.namespace('appointments', description='Manage Appointments')

appointment_booking = ns.model('AppointmentBooking', {
    'pet': fields.Integer(required=True, description='Pet\'s UID.', example=1),
    'employee': fields.Integer(required=True, description='Employee\'s UID.', example=1),
    'timeslot': fields.Integer(required=True, description='Timeslot\'s UID.', example=1),
    'date': fields.Date(required=True, description='The day of the appointment.', example='2022-07-14'),
})

def extra_validation(resources: AppointmentResources):
    payload_pet = api.payload['pet']
    payload_employee = api.payload['employee']
    payload_timeslot = api.payload['timeslot']
    payload_date = api.payload['date'] = datetime.strptime(api.payload['date'], "%Y-%m-%d").date()

    errors = {}

    if not resources.pet_exists(payload_pet):
        errors['pet'] = f'{payload_pet} does not reference an existing entity'

    if not resources.employee_exists(payload_employee):
        errors['employee'] = f'{payload_employee} does not reference an existing entity'

    if not resources.timeslot_exists(payload_timeslot):
        errors['timeslot'] = f'{payload_timeslot} does not reference an existing entity'

    if payload_date < date.today():
        errors['date'] = f'\'{payload_date}\' cannot be a date in the past'

    elif not errors.get('timeslot', None) and payload_date == date.today() and resources.get_timeslot_start(payload_timeslot) < datetime.now().time():
        errors['timeslot'] = 'Value cannot be a timeslot in the past'

    if errors:
        abort(400, errors=errors)

booked_appointment = ns.model('BookedAppointment', {
    'uid': fields.Integer(required=True, description='The booked appointment\'s UID.', example=1),
})

@ns.route('/')
class AppointmentAPI(Resource):
    @ns.doc(description='Book an appointment.')
    @ns.expect(appointment_booking, validate=True)
    @ns.marshal_with(booked_appointment, code=201, description='The appointment is booked.')
    @ns.response(400, 'One of the input fields is missing, has a wrong format, or an inconsistent value.')
    @ns.response(409, 'The requested booking conflicts with an existing appointment.')
    def post(self):
        resources = AppointmentResources()

        extra_validation(resources)

        if resources.pet_has_appointment(
            pet=api.payload['pet'],
            timeslot=api.payload['timeslot'],
            date=api.payload['date']
        ):
            abort(409, message='The pet is already booked.')

        if resources.pet_owner_has_appointment(
            pet=api.payload['pet'],
            employee=api.payload['employee'],
            timeslot=api.payload['timeslot'],
            date=api.payload['date']
        ):
            abort(409, message='Another pet is already booked.')

        if resources.employee_has_appointment(
            employee=api.payload['employee'],
            timeslot=api.payload['timeslot'],
            date=api.payload['date']
        ):
            abort(409, message='Employee is already booked.')

        created_uid = resources.create_appointment(
            pet=api.payload['pet'],
            employee=api.payload['employee'],
            timeslot=api.payload['timeslot'],
            date=api.payload['date']
        )

        return { "uid": created_uid }, 201

appointment_details = ns.model('AppointmentDetails', {
    'uid': fields.Integer(attribute='appointment_uid', required=True, description='The appointment\'s UID.', example=1),
    'date': fields.Date(attribute='appointment_date', required=True, description='The day of the appointment.', example='2021-07-14'),
    'timeslot': {
        'start': fields.String(attribute='appointment_start', required=True, description='The time of the start of the appointment.', example='09:00:00'),
        'end': fields.String(attribute='appointment_end', required=True, description='The time of the end of the appointment.', example='09:30:00'),
    },
    'employee': {
        'uid': fields.Integer(attribute='employee_uid', required=True, description='The employee\'s UID.', example=1),
        'name': fields.String(attribute='employee_name', required=True, description='The employee\'s name.', example='Carl Smith'),
        'employee_type': {
            'uid': fields.Integer(attribute='employee_type_uid', required=True, description='The employee type\'s UID.', example=1),
            'type': fields.String(attribute='employee_type', required=True, description='The employee type\'s title/label.', example='Veterinarian'),
        },
    },
    'practice': {
        'uid': fields.Integer(attribute='practice_uid', required=True, description='The practice\'s UID.', example=1),
        'name': fields.String(attribute='practice_name', required=True, description='The practice\'s name.', example='Plymouth Vets'),
        'telephone': fields.String(attribute='practice_telephone', required=True, description='The practice\'s telephone number.', example='01 752 000001'),
        'address': fields.String(attribute='practice_address', required=True, description='The practice\'s physical/s-mail address.', example='123 Test Street, Plymouth, Devon, PL1 1AA'),
    },
    'pet': {
        'uid': fields.Integer(attribute='pet_uid', required=True, description='The pet\'s UID.', example=1),
        'name': fields.String(attribute='pet_name', required=True, description='The pet\'s name.', example='Rex'),
        'animal': fields.String(attribute='pet_animal', required=True, description='The pet\'s species name.', example='Dog'),
        'breed': fields.String(attribute='pet_breed', required=False, description='The pet\'s breed, if any.', example='Bonkus'),
        'date_of_birth': fields.String(attribute='pet_date_of_birth', required=True, description='The pet\'s day of birth.', example='2019-12-24'),
    },
    'owner': {
        'uid': fields.Integer(attribute='owner_uid', required=True, description='The owner\'s UID.', example=1),
        'name': fields.String(attribute='owner_name', required=True, description='The owner\'s name.', example='Timmy Jerico'),
        'telephone': fields.String(attribute='owner_telephone', required=True, description='The owner\'s telepohne number.', example='07 465 000001'),
    },
    'is_cancelled': fields.Boolean(attribute='appointment_is_cancelled', required=True, description='Indicates whether or not the appointment was cancelled.'),
    'cancellation_reason': fields.String(attribute='appointment_cancellation_reason', required=False, description='If the appointment was cancelled, indicates the reason of the cancellation.'),
    'cancellation_time': fields.String(attribute='appointment_cancellation_time', required=False, description='If the appointment was cancelled, indicates day and time of the cancellation.', example='2021-12-17 18:30:00'),
})

appointment_cancellation = ns.model('AppointmentCancellation', {
    'reason': fields.String(required=False, description='The reason why the appointment is being cancelled.')
})

@ns.route('/<int:uid>')
class AppointmentItemAPI(Resource):
    @ns.doc(description='Get the details of an appointment.')
    @ns.response(200, 'The appointment details.')
    @ns.response(404, 'The appointment does not exist.')
    def get(self, uid: int):
        resources = AppointmentResources()

        raw_details = resources.get_appointment(uid)

        if not raw_details:
            abort(404)

        return marshal(raw_details, appointment_details), 200

    @ns.doc(description='Cancel an appointment.')
    @ns.expect(appointment_cancellation, validate=True)
    @ns.response(204, 'The appointment was cancelled.')
    @ns.response(400, 'One of the input fields is missing, has a wrong format, or an inconsistent value.')
    @ns.response(404, 'The appointment does not exist.')
    def delete(self, uid: int):
        resources = AppointmentResources()

        if not resources.cancel_appointment(uid, api.payload.get('reason') or 'No reason was provided for this cancellation.'):
            abort(404)

        return '', 204
