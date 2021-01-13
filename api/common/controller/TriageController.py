import psycopg2
import datetime
from common.controller.DataFrame import DataFrame

class TriageController:
    # Database connection information
    DATA = {
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
        # Retrieve previous years referal data from database
        initial_referal_data = self.get_initial_referal_data(self.params['start-date'])
        
        # Format and feed historic referal data into ML model to predict future referals
        initial_prediction_data = self.format_referal_data(initial_referal_data)
        predictions = self.get_predictions(self.params['intervals'], initial_prediction_data)

        # Retrieve a distribution prediction of patients by triage class
        distribution = self.get_triage_class_distribution(self.params['clinic-settings'])

        # Create the dataframe and run simulation
        data_frame = DataFrame(self.params['intervals'], predictions, distribution)
        # Note: Currently returns just the predictions variable 
        # but will return simulation results connected to the simulation module
        simulation_results = {
            'interval': predictions,
            'total': predictions
        }
        
        return simulation_results
        
    def get_initial_referal_data(self, start_date):
        # Calculate the (start date - a year) to search the database for relevant historic data
        previous_year_date = datetime.datetime.strptime(start_date, '%Y-%m-%d') - datetime.timedelta(days=365)
        
        # Establish database connection
        db = psycopg2.connect(
            database=self.DATA['database'],
            user=self.DATA['user'],
            password=self.DATA['password'],
            host=self.DATA['host'],
            port=self.DATA['port']
        )

        # Query for referal data from previous year
        cur = db.cursor()
        cur.execute(f"SELECT date_received \
                      FROM triagedata.historicdata \
                      WHERE date_received < %(previous_year_date)s::date \
                      ORDER BY date_received DESC \
                      FETCH FIRST 31 ROWS ONLY",
                      {
                          'previous_year_date': previous_year_date
                      })
        rows = cur.fetchall()
        db.close()

        # Return results
        return [date_seen[0] for date_seen in rows]

    def format_referal_data(self, referal_data):
        # Find the difference in days between historic referal datapoints
        return [(next_referal - previous_referal).days
                for previous_referal, next_referal
                in zip(referal_data[:-1], referal_data[1:])]

    def get_predictions(self, intervals, initial_prediction_data):
        # Return a list of predictions
        # Note: Currently hardcoded but will change when connected to the ML module
        return [(1, 1) for x in range(len(intervals))]

    def get_triage_class_distribution(self, clinic_settings):
        # Return a distribution of patient referals by triage class 
        # Note: Currently hard coded but will be calculated once more data is provided by the client
        return {
            1: 0.5,
            2: 0.2,
            3: 0.2,
            4: 0.1
        }