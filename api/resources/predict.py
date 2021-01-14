"""
This module handles all required interaction with the `/predict` endpoint
"""

# External dependencies
from flask_restful import Resource
from flask import request
from webargs.flaskparser import parser
from webargs import fields

# Internal dependencies
from api.common.controller.TriageController import TriageController
from api.common.database_interaction import DataBase


class Predict(Resource):
    """
    The `Predict` class handles all of the requests relative to Prediction for the API.
    """
    # Database connection information
    DATABASE_DATA = {
        'database': 'triage',
        'user': 'predict_handler',
        'password': 'password',
        'host': 'localhost',
        'port': '5432'
    }
    """
    This is the database connection information used by Predict to connect to the database. 
    See `api.common.database_interaction.DataBase` for configuration details and required arguments.
    """

    # API input schema
    arg_schema_get = {
        "clinic-id": fields.Int(required=True),
        "start-date": fields.String(required=True),
        "end-date": fields.String(required=True),
        "intervals": fields.List(fields.Raw(), missing=[]),
        "confidence": fields.Float(missing=0.95),
        "num-sim-runs": fields.Int(missing=1000),
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
                intervaled_slot_predictions (list) Predictions grouped by interval.
                number_intervals (int) Number of intervals.
                slot_predictions (list) Total predictions.
                models (list): A list of dictionaries representing each model
            }
            ```
            
        """
        # Validate input arguments.
        args = parser.parse(self.arg_schema_get, request,
                            location='querystring')
        # Retrieve clinic settings
        args['clinic-settings'] = self.get_clinic_settings(args['clinic-id'])
        # Instantiate TriageController
        triage_controller = TriageController(args)
        predictions = triage_controller.predict()
        # API response
        return {
            'url': request.url,
            'intervaled_slot_predictions': predictions['interval'],
            'number_intervals': len(args['intervals']),
            'slot_predictions': predictions['total']
        }

    def get_clinic_settings(self, clinic_id):
        """
        Retrieves clinic triage class settings for a given clinic id.

        Args:
            clinic_id (int): The ID of the clinic.

        Returns:
            A list of dictionaries for each triage class with
            ```
            {
                clinic_id (int) ID of the clinic.
                severity (int) Severity of the triage class
                name (str) Name of the triage class.
                duration (int) Time in weeks within which a patient should be seen.
                proportion (float) % of patients within the triage class that should be seen within the appropriate time.
            }
            ```
        """
        # Keys for response
        keys = ['clinic_id', 'severity', 'name', 'duration', 'proportion']
        # Establish database connection
        db = DataBase(self.DATABASE_DATA)
        # Query for data
        rows = db.select("SELECT clinic_id, severity, name, duration, proportion \
                          FROM triagedata.triageclasses \
                          WHERE clinic_id=%s", (clinic_id))
        # Return data
        return [dict(zip(keys, values)) for values in rows]
