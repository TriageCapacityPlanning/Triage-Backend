from flask_restful import Resource
from flask import request
from webargs.flaskparser import parser
from webargs import fields
from common.controller.TriageController import TriageController
from common.database_interaction import DataBase


class Predict(Resource):
    # Database connection information
    DATABASE_DATA = {
        'database': 'triage',
        'user': 'predict_handler',
        'password': 'password',
        'host': 'localhost',
        'port': '5432'
    }

    # API input schema
    arg_schema_get = {
        "clinic-id": fields.Int(required=True),
        "start-date": fields.String(required=True),
        "end-date": fields.String(required=True),
        "intervals": fields.List(fields.Raw(), missing=[]),
        "confidence": fields.Float(missing=0.95),
        "num-sim-runs": fields.Int(missing=1000),
        "waitlist": fields.Raw(missing=[])
    }

    def get(self):
        # Validate input arguments.
        args = parser.parse(self.arg_schema_get, request,
                            location='querystring')
        # Retrieve clinic settings
        args['clinic-settings'] = self.get_clinic_settings(args['clinic-id'])
        # Instantiate TriageController
        triage_controller = TriageController(args)
        predictions = triage_controller.predict()
        # API response
        return {
            'url': request.url,
            'intervaled_slot_predictions': predictions['interval'],
            'number_intervals': len(args['intervals']),
            'slot_predictions': predictions['total']
        }

    def get_clinic_settings(self, clinic_id):
        # Keys for response
        keys = ['clinic_id', 'severity', 'name', 'duration', 'proportion']
        # Establish database connection
        db = DataBase(self.DATABASE_DATA)
        # Query for data
        rows = db.select("SELECT clinic_id, severity, name, duration, proportion \
                          FROM triagedata.triageclasses \
                          WHERE clinic_id=%s", (clinic_id))
        # Return data
        return [dict(zip(keys, values)) for values in rows]
