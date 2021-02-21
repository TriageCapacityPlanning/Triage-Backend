"""
The Triage API to serve to the front end

Read the documentation from Flask: https://flask-restful.readthedocs.io/en/latest/
"""

from flask import Flask
from flask_restful import Api
from api.resources.predict import Predict
from api.resources.update_triage_classes import UpdateTriageClasses
from api.resources.models import Models
import api.resources.upload as Upload
from api.resources.data import Data


def create_app():
    app = Flask(__name__)
    api = Api(app)

    @app.route('/')
    def index():
        return {'status': 200, 'api': "Triage API", 'version': 1}

    @app.route('/v1')
    def version():
        return {'status': 200, 'version': 1}

    api.add_resource(Predict, '/predict')
    api.add_resource(Models, *['/models', '/models/use'])
    api.add_resource(UpdateTriageClasses, '/classes')
    api.add_resource(Upload.Waitlist, '/upload/waitlist')
    api.add_resource(Upload.PastAppointments, '/upload/past-appointments')
    api.add_resource(Upload.Model, '/upload/model')
    api.add_resource(Data, '/data/<clinic_id>/<triage_class>')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
