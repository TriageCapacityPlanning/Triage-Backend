"""
This module handles all required interaction with the `/upload` endpoints
"""

import csv
from typing import ClassVar

from flask_restful import Resource
from flask import request
from webargs.flaskparser import parser
from webargs import fields


# Internal dependencies
from api.common.database_interaction import DataBase


class Waitlist(Resource):
    def put(self):
        args = request.args.to_dict()
        print(request.files)
        return args


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
        'upload_data': fields.__file__
    }
    """
    The required schema to handle a put request

    Args:
        clinic_id (int): The id of the clinic uploading data
    """

    def put(self):
        print(request.files.get('upload_data').mimetype)
