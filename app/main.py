from app.validation import format_checker
from flask import Flask, Blueprint
from flask_restplus import Api

app = Flask(__name__)

blueprint = Blueprint('api', __name__, url_prefix='/api/v1.0')
api = Api(version="1.0", title="FF Technical Test", description="Sample REST API for Full Fibre Technical Test", format_checker=format_checker)

api.init_app(blueprint)
app.register_blueprint(blueprint)

from app.Appointments.appointments_endpoint import ns as appointments_namespace
api.add_namespace(appointments_namespace)
