"""
This module handles all required interaction with the `/data` endpoint
"""

# External dependencies
from flask import request
from webargs.flaskparser import parser
from webargs import fields
import ast

# Internal dependencies
from api.resources.AuthResource import AuthResource, authenticate
from api.common.ClinicData import ClinicData


class Data(AuthResource):
    """
    The `Data` class handles all of the requests relative to retrieving Data for the API.
    """

    # API input schema
    path_arg_schema_get = {
        "clinic_id": fields.Int(required=True),
        "triage_class": fields.Int(required=True)
    }
    """
    The required schema of path arguments to handle a get request

    Args:
        clinic_id (int): The id of the clinic being referenced.
        triage_class (int): The triage class severity level.
    """

    url_arg_schema_get = {
        "interval": fields.Raw(required=True)
    }
    """
    The required schema to handle a get request

    Args:
        intervals (tuple): 2-ary tuple with start and end date for desired data retrieval.
    """

    def get(self, clinic_id, triage_class):
        """
        Handles a get request for the data endpoints.
        
        Args:
            Requires api query string arguments, see `Data.url_arg_schema_get`, in the get request
            Requires api path arguments, see `Data.path_arg_schema_get`, in the get request

        Returns:
            Returns the list of tuples of historic data.
            The tuple sinclude the following information:
            1. Clinic id
            2. Triage class severity
            3. Referral arrival date
            4. Patient seen date
        """
        # Validate input arguments.
        path_args = parser.parse(self.path_arg_schema_get, request, location="path")
        url_args = parser.parse(self.url_arg_schema_get, request,
                                location='querystring')
        url_args['interval'] = ast.literal_eval(url_args['interval'])

        if type(url_args['interval']) != list or len(url_args['interval']) != 2:
            raise RuntimeError('Invalid Interval Input')

        clinic_data = ClinicData(path_args['clinic_id'])

        return clinic_data.get_referral_data(path_args['triage_class'], url_args['interval'])
