"""
This module handles all required interaction with the `/auth` endpoint
"""

# External dependencies
from flask_restful import Resource
from flask import request
from webargs.flaskparser import parser
from webargs import fields
import ast
import json
import jwt
import datetime

# Internal dependencies
from api.common.database_interaction import DataBase

SECRET_KEY = 'thisisthesecretkey'

class Auth(Resource):
    """
    The `Predict` class handles all of the requests relative to Prediction for the API.
    """

    DATABASE_DATA = {
        'database': 'triage',
        'user': 'admin',
        'password': 'docker',
        'host': 'db',
        'port': '5432'
    }
    """
    This is the database connection information used by PastAppointments to connect to the database.
    See `api.common.database_interaction.DataBase` for configuration details and required arguments.
    """

    # API input schema
    arg_schema_get = {
        "username": fields.Str(required=True),
        "password": fields.Str(required=True)
    }

    """
    The required schema to handle a get request

    Args:
        clinic_id (int): The id of the clinic being referenced.
        start_date (str): The start date of the predictions.
        end_date (str): The end date of the predictions.
        intervals (list): Date intervals for predictions to be grouped by.
        confidence (float): Required prediction confidence.
        num_sim_runs (int): Number of simulations to run.
        waitlist (file): Current wait list of patients for the clinic.
    """

    

    def get(self):
        """
        Handles a get request for the predict endpoints.
        Returns a dictionary with a list of predictions based on the ML model predictions and simulation runs.

        Args:
            Requires api query string arguments, see `Predict.arg_schema_get`, in the get request

        Returns:
            A dictionary with
            ```
            {
                url (str) The request url.
                intervaled_slot_predictions (list) Predictions grouped by interval.
                number_intervals (int) Number of intervals.
                slot_predictions (list) Total predictions.
                models (list): A list of dictionaries representing each model
            }
            ```

        """
        # Validate input arguments.
        args = parser.parse(self.arg_schema_get, request, location='querystring')
        
        user_clinic = self.__validate_user(args['username'], args['password'])

        return json.dumps({ 'token': self.__generate_token(args['username'], user_clinic), 'clinic_id': user_clinic })
            

    def __validate_user(self, username, password):
        db = DataBase(self.DATABASE_DATA)
        query = "SELECT clinic_id FROM triagedata.users "
        query += "WHERE username='%s' " % username
        query += "AND password='%s'" % password
        
        result = db.select(query)

        if len(result) > 0:
            return  result[0][0]
        else:
            raise RuntimeError('Invalid User Credentials')

    
    def __generate_token(self, username, user_clinic):
        return str(jwt.encode({
                'user': username,
                'clinic': user_clinic,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
            },
            SECRET_KEY, algorithm="HS256"))