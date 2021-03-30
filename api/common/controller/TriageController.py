"""
The TriageController is used to initiate prediction and simulation upon API requests.
"""

# External dependencies.
from datetime import datetime, timedelta
from collections import Counter, deque
import numpy as np
import triage_ml
import json

# Internal dependencies
from api.common.database_interaction import DataBase
from api.common.ClinicData import ClinicData
from api.common.controller.DataFrame import DataFrame
from sim.resources.minintervalschedule import gen_min_interval_slots, SimulationResults
from api.common.config import database_config

DATE_FORMAT = '%Y-%m-%d'


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
        'user': 'triage_controller',
        'password': 'password',
        'database': database_config['database'],
        'host': database_config['host'],
        'port': database_config['port']
    }
    """
    This is the database connection information used by Models to connect to the database.
    See `api.common.database_interaction.DataBase` for configuration details and required arguments.
    """

    PADDING_LENGTH = 30
    """
    Minimum padding length required by ML module.
    """

    # Constructor
    def __init__(self, clinic_id, intervals, confidence, num_sim_runs):
        self.clinic_id = clinic_id
        self.intervals = [{'start': datetime.strptime(interval['start'], DATE_FORMAT),
                           'end': datetime.strptime(interval['end'], DATE_FORMAT)}
                          for interval in intervals]
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

        results = {}

        clinic_data = ClinicData(self.clinic_id)

        for triage_class in clinic_data.get_clinic_settings():
            # Predict and simulate
            model = triage_ml.models.radius_variance.RadiusVariance(
                seq_size=30, radius=15, time_interval=triage_ml.data.dataset.TimeInterval.WEEK)
            model._init_model()
            model.model.load_weights(self.get_model(triage_class['severity']))
            dates = list([self.encode_date(self.intervals[0]['start'])])
            weeks = int(
                (self.intervals[-1]['end'] - self.intervals[0]['start']).days / 7)

            for i in range(weeks):
                dates.append(self.gen_next_date(dates[-1]))
            dates = np.stack(dates)

            padding_interval = self.__get_padding_interval(
                self.intervals[0]['start'], self.PADDING_LENGTH)
            padding_data = self.__sort_padding_data(clinic_data.get_referral_data(triage_class['severity'], padding_interval),
                                                    padding_interval[0],
                                                    self.PADDING_LENGTH)

            padding_data = np.array(padding_data)[:, np.newaxis]

            predictions = model.predict(
                [padding_data[np.newaxis, :], dates[0]], dates)
            predictions = [np.array(p)[0] for p in predictions]

            prediction_dataframe = DataFrame(
                [[p, 0] for p in padding_data] + predictions, self.intervals, self.PADDING_LENGTH)
            sim_results = gen_min_interval_slots(queue=deque(),
                                                 data_frame=prediction_dataframe,
                                                 start=1,
                                                 end=len(self.intervals),
                                                 min_ratio=triage_class['proportion'],
                                                 window=triage_class['duration'],
                                                 final_window=2 *
                                                 triage_class['duration'],
                                                 confidence=self.confidence)

            if sim_results:
                sim_result_formatted = [{'slots': sim_result[0].expected_slots,
                                         'start': sim_result[1]['start'].strftime(DATE_FORMAT),
                                         'end': sim_result[1]['end'].strftime(DATE_FORMAT)
                                         } for sim_result in zip(sim_results, self.intervals)]
            else:
                sim_result_formatted = [{'slots': 0,
                                         'start': interval['start'].strftime(DATE_FORMAT),
                                         'end': interval['end'].strftime(DATE_FORMAT)
                                         } for interval in self.intervals]

            results[triage_class['name']] = sim_result_formatted
        
        print(results)
        return results

    def encode_date(self, date):
        one_hot_date = np.zeros(12 + 31)
        one_hot_date[date.date().month] = 1
        one_hot_date[11 + date.date().day] = 1

        return one_hot_date

    def gen_next_date(self, date_encoding, days=7):
        month = np.argmax(date_encoding[:12]) + 1
        day = np.argmax(date_encoding[12:]) + 1
        date = datetime.strptime(
            f'2000/{0 if month < 10 else ""}{month}/{0 if day < 10 else ""}{day}', '%Y/%m/%d')
        date = date + timedelta(days=days)

        return self.encode_date(date)

    def __get_padding_interval(self, start_date, weeks):
        start = start_date - timedelta(weeks=30)
        newest_data_year = self.__get_historic_data_year(start)

        start = start.replace(year=newest_data_year)
        end = start + timedelta(weeks=30)

        return [start, end]

    def __get_historic_data_year(self, start_date):
        db = DataBase(self.DATABASE_DATA)

        year = db.select("SELECT EXTRACT(YEAR FROM historicdata.date_received) \
                         FROM triagedata.historicdata \
                         WHERE EXTRACT(MONTH FROM historicdata.date_received)= %(month)s AND \
                               EXTRACT(DAY FROM historicdata.date_received) >= %(day)s \
                         ORDER BY historicdata.date_received DESC \
                         FETCH FIRST 1 ROWS ONLY" %
                         {
                             'month': start_date.month,
                             'day': start_date.day
                         })

        if len(year) != 1:
            raise RuntimeError(
                'Could not find historic data year for start date: %s', start_date)

        return int(year[0][0])

    def __sort_padding_data(self, referral_data, start_date, weeks):
        """Sorts historic referral data by triage class.
        Parameters:
            `referral_data` (list(str)): List of historic referral dates.
        Returns:
            Returns a dictionary with a count of patient arrivals per day for each triage class.
        """
        result = []
        end_date = start_date + timedelta(weeks=1)

        partitioned_data = {}
        for referral in referral_data:
            week = int(
                (datetime.strptime(referral[2], DATE_FORMAT) - start_date).days / 7)
            if week in partitioned_data:
                partitioned_data[week] += 1
            else:
                partitioned_data[week] = 0

        return [partitioned_data[week] if week in partitioned_data else 0 for week in range(weeks)]

    def get_model(self, triage_class_severity):
        # Establish database connection
        db = DataBase(self.DATABASE_DATA)

        # Query for referral data from previous year
        rows = db.select("SELECT file_path \
                           FROM triagedata.models  \
                           WHERE clinic_id = %(clinic_id)s \
                           AND severity = %(severity)s \
                           AND in_use = %(in_use)s" %
                         {
                             'clinic_id': self.clinic_id,
                             'severity': triage_class_severity,
                             'in_use': True
                         })

        if len(rows) == 0:
            raise RuntimeError(
                'Could not find model for clinic %s, triage class %s', self.clinic_id, triage_class_severity)

        return rows[0][0]

    def get_predictions(self, model, data, start_date, prediction_length):
        """Runs ML model predictions and returns results.
        """
        predictions = []
        for offset in range(0, prediction_length):
            date = start_date + timedelta(days=offset)
            one_hot_date = np.zeros(12 + 31)
            one_hot_date[date.month] = 1
            one_hot_date[11 + date.day] = 1

            prediction = model.predict(
                [np.array(data)[np.newaxis, :], one_hot_date[np.newaxis, :]])
            predictions.append(prediction[0])

            data = data[1:] + [int(prediction[0][0])]
        return predictions
