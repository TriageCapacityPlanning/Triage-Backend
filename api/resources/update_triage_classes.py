"""
This module handles all required interaction with the `/classes` endpoint
"""

# External dependencies
from api.resources.AuthResource import AuthResource, authenticate
from flask import request
from webargs.flaskparser import parser
from webargs import fields

# Internal dependencies
from api.common.database_interaction import DataBase
from api.common.config import database_config
from api.common.ClinicData import ClinicData

class UpdateTriageClasses(AuthResource):
    """
    The `UpdateTriageClasses` class handles all of the requests relative to updating triage class data for the API.
    """

    DATABASE_DATA = {
        'user': 'triage_class_handler',
        'password': 'password',
        'database': database_config['database'],
        'host': database_config['host'],
        'port': database_config['port']
    }
    """
    This is the database connection information used by Models to connect to the database.
    See `api.common.database_interaction.DataBase` for configuration details and required arguments.
    """

    arg_schema_get = {
        'clinic_id': fields.Int(required=True)
    }
    """
    The required schema to handle a get request

    Args:
        clinic_id (int): The id of the clinic being referenced
    """

    arg_schema_put = {
        'triage_class': fields.Dict(required=True, keys=fields.Str(), values=fields.Raw())
    }
    """
    The required schema to hangle a patch request

    Args:
        triage_class (dict): A dictionary containing a triage classes information including
        ```
        {
            clinic_id (int): The ID of the clinic.
            severity (int): The severity level of the triage class.
            name (str): The name of the triage class.
            duration (int): The time (in weeks) within which a patient in the triage class should be seen.
            proportion (float): The proportion of patients in the triage class that must be seen in a reasonable time.
        }
        ```
    """

    def get(self):
        """
        Handles a get request for the classes endpoints.
        Returns a dictionary with a list of triage classes for an associated clinic.

        Args:
            Requires api query string arguments, see `UpdateTriageClasses.arg_schema_get`, in the get request

        Returns:
            A dictionary with
            `status` (int) The status of the request
            `classes` (list): A list of dictionaries representing each triage class.
        """

        # Validate input arguments.
        args = parser.parse(self.arg_schema_get, request,
                            location='querystring')
        # Retrieve triage classes from database
        clinic_data = ClinicData(args['clinic_id'])
        triage_classes = clinic_data.get_clinic_settings()
        # API Response
        return {'status': 200, 'classes': triage_classes}

    def put(self):
        """
        Handles a put request for the classes endpoints.
        Updates or creates a triage class in the database.

        Args:
            Requires api query string arguments, see `UpdateTriageClasses.arg_schema_put`, in the put request

        Returns:
            A dictionary with
            `status` (int) The status of the request
            `updated` (dict): The created or updated class.
        """
        # Validate input arguments
        args = parser.parse(self.arg_schema_put, request, location='json')

        # Update triage class in database
        clinic_data = ClinicData(args['triage_class']['clinic_id'])
        clinic_data.update_triage_class(args['triage_class'])

        # API Response
        return {'status': 200, 'updated': args['triage_class']}