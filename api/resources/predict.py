from flask_restful import Resource
from flask import request
import psycopg2
from webargs.flaskparser import parser
from webargs import fields, validate

predict_args = {
    "clinic-id": fields.Int(required=True),
    "start-date": fields.String(required=True),
    "end-date": fields.String(required=True),
    "intervals": fields.List(fields.String),
    "confidence": fields.Float(missing=0.95),
    "num-sim-runs": fields.Int(missing=1000),
    "waitlist": fields.Raw(missing=[])
}

class Predict(Resource):
    def get(self):
        # Validate input arguments.
        args = parser.parse(predict_args, request, location='querystring')

        # Retrieve clinic settings
        clinic_settings = self.getClinicSettings(args['clinic-id'])

        # Trigger Simulation
        pass

        # Return result
        return args

    def getClinicSettings(self, clinic_id):
        return {}