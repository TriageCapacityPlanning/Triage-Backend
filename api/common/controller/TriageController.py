"""
The TriageController is used to initiate prediction and simulation upon API requests.
"""

# External dependencies.
from datetime import datetime, timedelta
from api.common.database_interaction import DataBase


class TriageController:
    """
    TriageController is a class to handle API requests to run predictions and simulations.

    Usage:
        To create a new triage controller, create it with `TriageController(intervals, clinic_settings)` where
        those values are:
        ```
        {
            'intervals' (list(tuples(str))) List of start and end date strings for each interval.
            'clinic_settings' (dict) List of triage classes for the clinic.
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
    """
    This is the database connection information used by Models to connect to the database.
    See `api.common.database_interaction.DataBase` for configuration details and required arguments.
    """

    PADDING_LENGTH_MIN = 30
    """
    Minimum padding length required by ML module.
    """

    # Constructor
    def __init__(self, intervals, clinic_settings, padding_length):
        self.start_date = intervals[0][0]
        self.intervals = intervals
        self.clinic_settings = clinic_settings
        self.padding_length = padding_length

    def predict(self):
        """Returns the prediction / simulation results.

        Returns:
            Simulation results as a dictionary with the following key-value pairs:
            ```
            {
                interval (list(dict(str, int))): The referral count predictions for each interval per triage class.
                total (int): The referral count predictions in total per triage class.
            }
            ```

        """
        desired_historic_data_year = self.get_historic_data_year(self.intervals[0][0])

        # Retrieve previous years referral data from database
        padding = max(self.PADDING_LENGTH_MIN, self.padding_length)
        historic_data = self.get_historic_data_referrals(self.start_date, desired_historic_data_year, padding)

        # Sort referral_data by triage class.
        sorted_referral_data = self.sort_referral_data(historic_data, self.clinic_settings)

        # Run predictions
        pass

        # Create DataFrame
        pass

        # Run Simulations
        pass

        return {'interval': sorted_referral_data, 'total': sorted_referral_data}

    def get_historic_data_year(self, start_date):
        db = DataBase(self.DATABASE_DATA)

        year = db.select("SELECT EXTRACT(YEAR FROM historicdata.date_received) \
                         FROM triagedata.historicdata \
                         WHERE EXTRACT(MONTH FROM historicdata.date_received)= %(month)s AND \
                               EXTRACT(DAY FROM historicdata.date_received) >= %(day)s \
                         ORDER BY historicdata.date_received DESC \
                         FETCH FIRST 1 ROWS ONLY" %
                         {
                             'month': datetime.strptime(start_date, '%Y-%m-%d').month,
                             'day': datetime.strptime(start_date, '%Y-%m-%d').day
                         })

        if len(year) != 1:
            raise RuntimeError('Could not find historic data year for start date: %s', start_date)

        return int(year[0][0])

    def get_historic_data_referrals(self, start_date, historic_data_year, length):
        """Returns historic referral data to use as a start for running ML predictions.

        Parameters:
            `start_date` (str): The start date for predictions.
            `historic_data_year` (str): The year of historic data to query data from.
            `length` (int): The number of days to retrieve historic data for.
        Returns:
            A list of historic referral datapoints.
        """

        # Calculate the start and end dates for data retrieval.
        end_date = datetime.strptime(start_date, '%Y-%m-%d').replace(year=historic_data_year)
        start_date = (end_date - timedelta(days=length))

        # Establish database connection
        db = DataBase(self.DATABASE_DATA)

        # Query for referral data from previous year
        rows = db.select("SELECT historicdata.date_received, historicdata.date_seen \
                           FROM triagedata.historicdata \
                           WHERE historicdata.date_received >= '%(start_date)s'::date \
                                 AND historicdata.date_received < '%(end_date)s'::date" %
                         {
                             'start_date': start_date,
                             'end_date': end_date
                         })

        # Return results
        referral_data = [{'date_recieved': referral_data[0], 'date_seen': referral_data[1]} for referral_data in rows]
        return referral_data

    def sort_referral_data(self, referral_data, clinic_settings):
        """Sorts historic referral data by triage class.

        Parameters:
            `referral_data` (list(str)): List of historic referral dates.
            `clinic_settings` (list): List of clinic triage classes.
        Returns:
            Returns a dictionary with a count of patient arrivals per day for each triage class.
        """

        sorted_referral_data = {triage_class['severity']: [] for triage_class in clinic_settings}

        for referral in referral_data:
            wait_time = (referral['date_seen'] - referral['date_recieved']).days / 7

            possible_classes = []
            for triage_class in clinic_settings:
                if triage_class['duration'] >= wait_time:
                    possible_classes.append(triage_class['severity'])
            sorted_class = min(possible_classes) if len(possible_classes) > 0 else 1

            sorted_referral_data[sorted_class].append(referral['date_recieved'].strftime('%Y-%m-%d'))

        return sorted_referral_data

    def get_predictions(self, intervals, initial_prediction_data):
        """Runs ML model predictions and returns results.
        """
        assert NotImplementedError

    def run_simulation(self):
        """Runs simulation module.
        """
        assert NotImplementedError
