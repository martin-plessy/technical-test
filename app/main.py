from flask import Flask, Blueprint
from flask_restplus import Api

import sys
sys.path.append('.')

app = Flask(__name__)

blueprint = Blueprint('api', __name__, url_prefix='/api/v1.0')
api = Api(version="1.0", title="FF Technical Test", description="Sample REST API for Full Fibre Technical Test")

api.init_app(blueprint)
app.register_blueprint(blueprint)

from app.Appointments.appointments_endpoint import ns as appointments_namespace
api.add_namespace(appointments_namespace)
