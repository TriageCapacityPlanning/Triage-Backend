""" The Triage API to serve to the front end """

''' Read the documentation from Flask: https://flask-restful.readthedocs.io/en/latest/'''
from flask import Flask
from flask_restful import Api
from resources.predict import Predict
<<<<<<< HEAD
from resources.update_triage_classes import UpdateTriageClasses
from resources.models import Models, Use
=======
import resources.upload as Upload
>>>>>>> upload endpoints boilerplate

app = Flask(__name__)
api = Api(app)

api.add_resource(Predict, '/predict')
<<<<<<< HEAD
api.add_resource(Models, '/models')
api.add_resource(Use, '/models/use')
api.add_resource(UpdateTriageClasses, '/classes')
=======
api.add_resource(Upload.Waitlist, '/upload/waitlist')
api.add_resource(Upload.PastAppointments, '/upload/past-appointments')
>>>>>>> upload endpoints boilerplate

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"), debug=True)