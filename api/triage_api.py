"""
The Triage API to serve to the front end
Read the documentation from Flask: https://flask-restful.readthedocs.io/en/latest/
"""

from api.common.exceptions import FileError, Unauthorized
from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from api.resources.update_triage_classes import UpdateTriageClasses
from api.resources.models import Models
import api.resources.upload as Upload
from api.resources.data import Data
from api.resources.auth import Auth
from api.common.config import VERSION_PREFIX


def create_app():
    app = Flask(__name__)
    api = Api(app)

    @app.route('/')
    def index():
        return {'status': 200, 'api': "Triage API", 'version': 1}

    @app.route(VERSION_PREFIX)
    def version():
        return {'status': 200, 'version': 1}

    app.config["PROPAGATE_EXCEPTIONS"] = True

    @app.errorhandler(Unauthorized)
    def handle_unauthorized_user(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(FileError)
    def handle_file_upload_errors(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    try:
        from api.resources.predict import Predict
        api.add_resource(Predict, VERSION_PREFIX + '/predict')
    except ImportError:
        print("Could not import predict")

    api.add_resource(Models, *[VERSION_PREFIX + '/models', VERSION_PREFIX + '/models/use'])
    api.add_resource(UpdateTriageClasses, VERSION_PREFIX + '/classes')
    api.add_resource(Upload.PastAppointments, VERSION_PREFIX + '/upload/past-appointments')
    api.add_resource(Upload.Model, VERSION_PREFIX + '/upload/model')
    api.add_resource(Data, VERSION_PREFIX + '/data/<clinic_id>/<triage_class>')
    api.add_resource(Auth, VERSION_PREFIX + '/auth/login')
    CORS(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
