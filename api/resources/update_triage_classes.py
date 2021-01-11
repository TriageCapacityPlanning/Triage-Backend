from flask_restful import Resource
from flask import request
import psycopg2
from webargs.flaskparser import parser
from webargs import fields, validate
import json


class UpdateTriageClasses(Resource):
    DATA = {
        'database': 'triage',
        'user': 'admin',
        'password': 'password',
        'host': 'localhost',
        'port': '5432'
    }

    arg_schema_get = {
        'clinic-id': fields.Int(required=True)
    }

    arg_schema_put = {
        'triage-class': fields.Dict(required=True, keys=fields.Str(), values=fields.Raw())
    }

    def get(self):
        # Validate input arguments.
        args = parser.parse(self.arg_schema_get, request,
                            location='querystring')

        # Retrieve triage classes from database
        triage_classes = self.get_triage_classes(args['clinic-id'])

        # API Response
        return {'status': 200, 'classes': triage_classes}

    def put(self):
        # Validate input arguments
        args = parser.parse(self.arg_schema_put, request)

        # Update triage class in database
        self.update_triage_class(args['triage-class'])

        # API Response
        return {'status': 200, 'updated': args['triage-class']}

    def get_triage_classes(self, clinic_id):
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

    def update_triage_class(self, triage_class):
        # Establish database connection
        db = psycopg2.connect(
            database=self.DATA['database'],
            user=self.DATA['user'],
            password=self.DATA['password'],
            host=self.DATA['host'],
            port=self.DATA['port']
        )

        # Insert or update information
        cur = db.cursor()
        cur.execute(f"INSERT INTO triagedata.triageclasses (clinic_id, severity, name, duration, proportion) \
                      VALUES(%(clinic_id)s, \
                             %(severity)s, \
                             %(name)s, \
                             %(duration)s, \
                             %(proportion)s) \
                      ON CONFLICT ON CONSTRAINT pk DO UPDATE \
                        SET name = %(name)s, \
                            duration = %(duration)s, \
                            proportion = %(proportion)s",
                    {
                        'clinic_id': triage_class['clinic-id'],
                        'severity': triage_class['severity'],
                        'name': triage_class['name'],
                        'duration': triage_class['duration'],
                        'proportion': triage_class['proportion']
                    })
        db.commit()
        db.close()
