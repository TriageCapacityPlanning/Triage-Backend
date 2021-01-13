from common.database_interaction import DataBase
from flask_restful import Resource
from flask import request
from webargs.flaskparser import parser
from webargs import fields


class Models(Resource):
    DATABASE_DATA = {
        'database': 'triage',
        'user': 'model_handler',
        'password': 'password',
        'host': 'localhost',
        'port': '5432'
    }

    arg_schema_get = {
        'clinic-id': fields.Int(required=True)
    }

    arg_schema_patch = {
        'clinic-id': fields.Int(required=True),
        'model-id': fields.Int(required=True)
    }

    def get(self):
        # Validate input arguments.
        args = parser.parse(self.arg_schema_get, request,
                            location='querystring')
        # Retrieve clinic models from database
        models = self.get_clinic_models(args['clinic-id'])
        # API Response
        return {'status': 200, 'models': models}

    def patch(self):
        # Validate input arguments.
        args = parser.parse(self.arg_schema_patch, request,
                            location='querystring')
        # Update current active model for clinic-id to model-id
        self.set_active_model(args['clinic-id'], args['model-id'])
        # API Response
        return {'status': 200, 'model-id': args['model-id']}

    def set_active_model(self, clinic_id, model_id):
        # Establish database connection
        db = DataBase(self.DATABASE_DATA)
        # Update database data
        db.update("UPDATE triagedata.models \
                    SET in_use = (CASE WHEN id=%(model-id)s THEN true \
                                       ELSE false \
                                  END) \
                    WHERE clinic_id=%(clinic-id)s AND \
                          EXISTS ( \
                                SELECT id \
                                FROM triagedata.models \
                                WHERE clinic_id=%(clinic-id)s AND \
                                        id=%(model-id)s \
                                )", 
                    {'model-id': model_id, 'clinic-id': clinic_id})

    def get_clinic_models(self, clinic_id):
        # Keys for response
        keys = ['id', 'accuracy', 'created', 'in_use']
        # Establish database connection and get the data
        db = DataBase(self.DATABASE_DATA)
        rows = db.select("SELECT id, accuracy, to_char(created,'DD-MM-YYYY'), in_use \
                           FROM triagedata.models \
                           WHERE clinic_id=%s", (clinic_id))
        # Return data
        return [dict(zip(keys, values)) for values in rows]
