""" 
The TriageController is used to initiate prediction and simulation upon API requests.
"""

# External dependencies.
import datetime
from api.common.controller.DataFrame import DataFrame
from api.common.database_interaction import DataBase


class TriageController:
    """
    TriageController is a class to handle API requests to run predictions and simulations.

    Usage:
        To create a new triage controller, create it with `TriageController(params)` where
        params is a dictionary with the following keys:
        ```
        {
            'start-date' (str) Start date for the predictions,
            'end-date'     (str) End date for the predictions,
            'intervals'    (list(tuples(str))) Date intervals that predictions are made for,
            'clinic-id' (int) The ID of the clinic.
        }
        ```
    """

    # Database connection information
    DATABASE_DATA = {
        'database': 'triage',
        'user': 'triage_controller',
        'password': 'password',
        'host': 'localhost',
        'port': '5432'
    }

    # Constructor
    def __init__(self, params):
        self.params = params

    def predict(self):
        '''Returns the start and end date for a given interval.

        Returns:
            Simulation results as a dictionary with the following key-value pairs:
            ```
            {
                interval (list(dict(str, int))): The referal count predictions for each interval per triage class.
                total (int): The referal count predictions in total per triage class.
            }
            ```

        '''
        # Retrieve previous years referal data from database
        initial_referal_data = self.get_initial_referal_data(
            self.params['start-date'])

        # Format and feed historic referal data into ML model to predict future referals
        initial_prediction_data = self.format_referal_data(
            initial_referal_data)
        predictions = self.get_predictions(
            self.params['intervals'], initial_prediction_data)

        # Retrieve a distribution prediction of patients by triage class
        distribution = self.get_triage_class_distribution(
            self.params['clinic-settings'])

        # Create the dataframe and run simulation
        data_frame = DataFrame(
            self.params['intervals'], predictions, distribution)
        # Note: Currently returns just the predictions variable
        # but will return simulation results connected to the simulation module
        simulation_results = {
            'interval': predictions,
            'total': predictions
        }

        return simulation_results

    def get_initial_referal_data(self, start_date):
        '''Returns historic referal data to use as a start for running ML predictions.

        Parameters:
            `start-date` (str): The start date for predictions.
        Returns:
            A list of historic referal datapoints.
        '''
        # Calculate the (start date - a year) to search the database for relevant historic data
        previous_year_date = datetime.datetime.strptime(
            start_date, '%Y-%m-%d') - datetime.timedelta(days=365)

        # Establish database connection
        db = DataBase(self.DATABASE_DATA)

        # Query for referal data from previous year
        rows = db.select(f"SELECT date_received \
                           FROM triagedata.historicdata \
                           WHERE date_received < %(previous_year_date)s::date \
                           ORDER BY date_received DESC \
                           FETCH FIRST 31 ROWS ONLY",
                         {
                             'previous_year_date': previous_year_date
                         })

        # Return results
        return [date_seen[0] for date_seen in rows]

    def format_referal_data(self, referal_data):
        '''Formats historic referal data to be provided to the ML model.

        Parameters:
            `referal-data` (list(str)): List of historic referal dates.
        Returns:
            Returns a list of differences in time (days) between historic referal dates.
        '''
        # Find the difference in days between historic referal datapoints
        return [(next_referal - previous_referal).days
                for previous_referal, next_referal
                in zip(referal_data[:-1], referal_data[1:])]

    def get_predictions(self, intervals, initial_prediction_data):
        '''Runs ML model predictions and returns results.

        Parameters:
            `intervals` (list(tuple(str))): The list of date intervals to make predictions for.
            `initial_prediction_data` (list(int)): List of historic referal date differences.
        Returns:
            A list of predictions for each interval of time including a predicted referal count and variability.
        '''
        # Return a list of predictions
        # Note: Currently hardcoded but will change when connected to the ML module
        return [(1, 1) for x in range(len(intervals))]

    def get_triage_class_distribution(self, clinic_settings):
        '''Returns the distribution of patients for a given clinic by triage class.

        Parameters:
            `clinic_settings` (dict(string, any)): Set of clinic specific settings including triage classes and their expected distributions.
        Returns:
            A dictionary with keys being triage class severity and values being their expected % distirbution relative to total patients for the clinic.
        '''
        # Return a distribution of patient referals by triage class
        # Note: Currently hard coded but will be calculated once more data is provided by the client
        return {
            1: 0.5,
            2: 0.2,
            3: 0.2,
            4: 0.1
        }
