from flask import abort, request
from flask_restplus import Resource, abort

from app.Appointments.appointments_resources import AppointmentResources
resources = AppointmentResources()

from app.main import api
ns = api.namespace("appointments", description="Manage Appointments")


@ns.route('')
class AppointmentAPI(Resource):
    pass
