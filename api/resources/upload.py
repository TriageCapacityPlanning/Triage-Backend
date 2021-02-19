"""
This module handles all required interaction with the `/upload` endpoints
"""
from flask_restful import Resource
from flask import request
# from webargs.flaskparser import parser
from webargs import fields


# Internal dependencies
from api.common.database_interaction import DataBase


class Waitlist(Resource):
    def put(self):
        raise NotImplementedError()


class PastAppointments(Resource):
    """
    The `PastAppointments` class handles all of the requests relative to historic
    triage data for the API.
    """
    DATABASE_DATA = {
        'database': 'triage',
        'user': 'historic_data_handler',
        'password': 'password',
        'host': 'localhost',
        'port': '5432'
    }
    """
    This is the database connection information used by PastAppointments to connect to the database.
    See `api.common.database_interaction.DataBase` for configuration details and required arguments.
    """

    arg_schema_put = {
        'clinic_id': fields.Int(required=True),
        'upload_data': fields.Raw(required=True)
    }
    """
    The required schema to handle a put request

    Args:
        clinic_id (int): The id of the clinic uploading data
    """

    def put(self):
        # Figure out how to validate inputs
        mime_type = request.files.get('upload_data').mimetype
        if mime_type == 'text/csv':
            return self.upload_csv_data(request.files.get('upload_data'))
        else:
            raise TypeError('Unsupported file type uploaded')

    def upload_csv_data(self, upload_file):
        db = DataBase(self.DATABASE_DATA)
        db.insert_data_from_file(
                'triagedata.historicdata',
                ('clinic_id', 'date_received', 'date_seen'),
                upload_file,
                ','
            )


class Model(Resource):
    arg_schema_post = {
        'clinic_id': fields.Int(required=True),
        'model_weights': fields.Raw(required=True),
        'accuracy': fields.Float(required=True),
        'make_in_use': fields.Boolean(),
    }
    """
    The required schema to handle a post request

    Args:
        clinic_id (int): The id of the clinic uploading data
        model_weights (byte array): The model weights data
        accuracy (float): The accuracy for the given model
        make_in_use (bool): (Optional) Make the model in use for the clinic
    """
    def post(self):
        raise NotImplementedError()
