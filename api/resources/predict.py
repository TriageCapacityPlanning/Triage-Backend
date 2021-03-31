"""
This module handles all required interaction with the `/predict` endpoint
"""

# External dependencies
from flask import request
from webargs.flaskparser import parser
from webargs import fields
import ast

# Internal dependencies
from api.resources.AuthResource import AuthResource
from api.common.controller.TriageController import TriageController
from api.common.config import database_config


class Predict(AuthResource):
    """
    The `Predict` class handles all of the requests relative to Prediction for the API.
    """
    # Database connection information
    DATABASE_DATA = {
        'user': 'predict_handler',
        'password': 'password',
        'database': database_config['database'],
        'host': database_config['host'],
        'port': database_config['port']
    }
    """
    This is the database connection information used by Predict to connect to the database.
    See `api.common.database_interaction.DataBase` for configuration details and required arguments.
    """

    # API input schema
    arg_schema_get = {
        "clinic-id": fields.Int(required=True),
        "intervals": fields.String(missing="[]"),
        "confidence": fields.Float(missing=0.95),
        "num-sim-runs": fields.Int(missing=100),
        "waitlist": fields.Raw(missing=[])
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
                predictions (dict) Dictionary containing the interval predictions for each class.
            }
            ```

            The keys of the predictions dict are the triage class names and the values are lists of dicts of
            the following format:
            ```
            {
                'start' (str) Start date of the interval
                'end' (str) End date of the interval
                'slots' (int) Predicted slots.
            }
            ```

        """
        # Validate input arguments.
        args = parser.parse(self.arg_schema_get, request,
                            location='querystring')
        args['intervals'] = ast.literal_eval(args['intervals'])

        triage_controller = TriageController(args['clinic-id'],
                                             args['intervals'],
                                             args['confidence'],
                                             args['num-sim-runs'])
        predictions = triage_controller.predict()

        # API response
        return {
            'url': request.url,
            'predictions': predictions
        }
