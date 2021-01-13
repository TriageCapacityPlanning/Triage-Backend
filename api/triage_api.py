""" 
The Triage API to serve to the front end 

Read the documentation from Flask: https://flask-restful.readthedocs.io/en/latest/
"""

from flask import Flask
from flask_restful import Api
from resources.predict import Predict
from resources.update_triage_classes import UpdateTriageClasses
from resources.models import Models
import resources.upload as Upload
app = Flask(__name__)
api = Api(app)

api.add_resource(Predict, '/predict')
api.add_resource(Models, *['/models', '/models/use'])
api.add_resource(UpdateTriageClasses, '/classes')
api.add_resource(Upload.Waitlist, '/upload/waitlist')
api.add_resource(Upload.PastAppointments, '/upload/past-appointments')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
