"""
This module handles all required interaction with the `/predict` endpoint
"""

# External dependencies
from flask_restful import Resource
from flask import request
from webargs.flaskparser import parser
from webargs import fields
import ast
import json

# Internal dependencies
from api.common.ClinicData import ClinicData


class Data(Resource):
    """
    The `Predict` class handles all of the requests relative to Prediction for the API.
    """

    # API input schema
    path_arg_schema_get = {
        "clinic_id": fields.Int(required=True),
        "triage_class": fields.Int(required=True)
    }

    url_arg_schema_get = {
        "interval": fields.Raw(required=True)
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

    def get(self, clinic_id, triage_class):
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
        path_args = parser.parse(self.path_arg_schema_get, request, location="path")
        url_args = parser.parse(self.url_arg_schema_get, request,
                            location='querystring')
        url_args['interval'] = ast.literal_eval(url_args['interval'])

        clinic_data = ClinicData(path_args['clinic_id'])

        return clinic_data.get_referral_data(path_args['triage_class'], url_args['interval'])