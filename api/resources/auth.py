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

SECRET_KEY = 'thisisthesecretkey'

class Auth(Resource):
    """
    The `Predict` class handles all of the requests relative to Prediction for the API.
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
        
        valid_user, user_clinic = self.__validate_user(args['username'], args['password'])

        if(valid_user):
            return json.dumps({ 'token': self.__generate_token(args['username'], user_clinic).decode('UTF-8') })

        else:
            raise RuntimeError('Invalid User Credentials')

    def __validate_user(self, username, password):
        return True, 1
    
    def __generate_token(self, username, user_clinic):
        return jwt.encode({
                'user': username,
                'clinic': user_clinic,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
            },
            SECRET_KEY)