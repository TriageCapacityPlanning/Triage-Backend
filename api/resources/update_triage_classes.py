from flask_restful import Resource
from flask import request
import psycopg2
from webargs.flaskparser import parser
from webargs import fields, validate


class UpdateTriageClasses(Resource):
    DATA = {
        'database': 'triage',
        'user': 'admin',
        'password': 'password',
        'host': 'localhost',
        'port': '5432'
    }

    arg_schema_get = {
        "clinic-id": fields.Int(required=True)
    }

    def get(self):
        # Validate input arguments.
        args = parser.parse(self.arg_schema_get, request, location='querystring')

        # Retrieve triage classes from database
        triage_classes = self.get_triage_classes(args['clinic-id'])

        # Return data
        return {'status': 200, 'classes': triage_classes}

    def get_triage_classes(self, clinic_id):
        keys = ['id', 'clinic_id', 'severity', 'name', 'duration', 'proportion']
        db = psycopg2.connect(
            database=self.DATA['database'],
            user=self.DATA['user'],
            password=self.DATA['password'],
            host=self.DATA['host'],
            port=self.DATA['port']
        )

        cur = db.cursor()
        cur.execute(f"SELECT id, clinic_id, severity, name, duration, proportion \
                      FROM triagedata.triageclasses \
                      WHERE clinic_id={clinic_id}")
        rows = cur.fetchall()
        print(rows)
        db.close()
        return [dict(zip(keys, values)) for values in rows]