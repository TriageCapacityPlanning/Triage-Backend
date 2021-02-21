"""
The TriageController is used to initiate prediction and simulation upon API requests.
"""

# External dependencies.
from datetime import datetime, timedelta
from collections import Counter, deque

# Internal dependencies
from api.common.database_interaction import DataBase
from api.common.ClinicData import ClinicData
from api.common.controller.DataFrame import DataFrame
from sim.resources.minintervalschedule import gen_min_interval_slots, SimulationResults

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
        'host': 'db',
        'port': '5432'
    }
    """
    This is the database connection information used by Models to connect to the database.
    See `api.common.database_interaction.DataBase` for configuration details and required arguments.
    """

    ML_PADDING_LENGTH = 30
    SIM_PADDING_LENGTH = 7
    """
    Minimum padding length required by ML module.
    """

    # Constructor
    def __init__(self, clinic_id, intervals, confidence, num_sim_runs):
        self.clinic_id = clinic_id
        self.intervals = intervals
        self.confidence = confidence
        self.num_sim_runs = num_sim_runs

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
        # Find the year of the most recent historic data.
        historic_data_interval_length = max(self.ML_PADDING_LENGTH, self.SIM_PADDING_LENGTH)
        desired_historic_data_year = self.get_historic_data_year(self.intervals[0][0])
        historic_data_end_date = datetime.strptime(self.intervals[0][0], '%Y-%m-%d').replace(year=desired_historic_data_year)
        historic_data_interval = (historic_data_end_date - timedelta(days=historic_data_interval_length), 
                                  historic_data_end_date)

        # Retrieve historic referral data
        clinic_data = ClinicData(self.clinic_id)
        
        response = {}
        for triage_class in clinic_data.clinic_settings:
            historic_data = clinic_data.get_referral_data(triage_class['severity'], historic_data_interval)
            sorted_referral_data = self.sort_referral_data(historic_data, 
                                                           historic_data_interval[0],
                                                           historic_data_interval_length)
            

            # PASS SORTED_REFERAL_DATA TO MODEL
            predictions = [(5,1)] * 50
            
            # Create DataFrame
            data_frame = DataFrame(self.intervals, predictions, (self.SIM_PADDING_LENGTH, self.SIM_PADDING_LENGTH))

            # Run Simulation
            sim_results = gen_min_interval_slots(data_frame=data_frame, 
                                                 window=triage_class['duration'] * 7, 
                                                 min_ratio=triage_class['proportion'],
                                                 final_window=triage_class['duration'] * 14,
                                                 confidence=self.confidence,
                                                 start=0,
                                                 end=len(self.intervals),
                                                 num_sim_runs=self.num_sim_runs,
                                                 queue=deque()
                                                 )
            sim_result_formatted = [{'slots': sim_result[0].expected_slots,
                                  'start_date': sim_result[1][0],
                                  'end_date': sim_result[1][0]
                                  } for sim_result in zip(sim_results, self.intervals)]
            
            response[triage_class['name']] = sim_result_formatted
        return response

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

    def sort_referral_data(self, referral_data, start_date, interval_length):
        """Sorts historic referral data by triage class.

        Parameters:
            `referral_data` (list(str)): List of historic referral dates.
        Returns:
            Returns a dictionary with a count of patient arrivals per day for each triage class.
        """
        date_list = [(start_date + timedelta(days=offset)).strftime('%Y-%m-%d')
                      for offset in range(interval_length)]
        counted_data = Counter(referral[2] for referral in referral_data)
        
        return [counted_data[date] if date in counted_data else 0 for date in date_list]

    def get_model(self, clinic_id, triage_class):
        # Establish database connection
        db = DataBase(self.DATABASE_DATA)

        # Query for referral data from previous year
        rows = db.select("SELECT data \
                           FROM triagedata.models \
                           WHERE clinic_id = %(clinic_id)s \
                               AND severity = %(severity)s \
                                AND in_use = TRUE" %
                         {
                             'clinic_id': clinic_id,
                             'severity': triage_class
                         })

        return rows[0]

    def get_predictions(self, intervals, initial_prediction_data):
        """Runs ML model predictions and returns results.
        """
        assert NotImplementedError

    def run_simulation(self):
        """Runs simulation module.
        """
        assert NotImplementedError
