from app.Appointments.appointments_resources import AppointmentResources
from app.main import api
from datetime import date, datetime, time
from flask_restplus import abort, fields, Resource

ns = api.namespace('appointments', description='Manage Appointments')

appointment_booking = api.model('AppointmentBooking', {
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

booked_appointment = api.model('BookedAppointment', {
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
