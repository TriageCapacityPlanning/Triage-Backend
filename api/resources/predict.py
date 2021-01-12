from flask_restful import Resource
from flask import request
import psycopg2
from webargs.flaskparser import parser
from webargs import fields, validate
from common.controller.TriageController import TriageController

class Predict(Resource):
    # Database connection information
    DATA = {
        'database': 'triage',
        'user': 'admin',
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
        args = parser.parse(self.arg_schema_get, request, location='querystring')

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
        keys = ['clinic_id', 'severity',
                'name', 'duration', 'proportion']

        # Establish database connection
        db = psycopg2.connect(
            database=self.DATA['database'],
            user=self.DATA['user'],
            password=self.DATA['password'],
            host=self.DATA['host'],
            port=self.DATA['port']
        )

        # Query for data
        cur = db.cursor()
        cur.execute(f"SELECT clinic_id, severity, name, duration, proportion \
                      FROM triagedata.triageclasses \
                      WHERE clinic_id=%(clinic_id)s",
                    {
                        'clinic_id': clinic_id
                    })
        rows = cur.fetchall()
        db.close()

        # Return data
        return [dict(zip(keys, values)) for values in rows]
