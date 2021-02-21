"""
The Historic is used to retrieve historic referral data from the database.
"""

# External dependencies.
from datetime import datetime, timedelta
from api.common.database_interaction import DataBase


class ClinicData:
    """
    Historic is a class to retrieve historic referral data from the database module.

    Usage:
        To create a new HistoricData object, create it with `HistoricData(clinic_id)` where
        those values are:
        ```
        {
            'clinic_id' (int) The ID value of the clinic for which data is needed.
        }
        ```
    """

    # Database connection information
    DATABASE_DATA = {
        'database': 'triage',
        'user': 'admin',
        'password': 'password',
        'host': 'db',
        'port': '5432'
    }
    """
    This is the database connection information used by HistoricData to connect to the database.
    See `api.common.database_interaction.DataBase` for configuration details and required arguments.
    """


    # Constructor
    def __init__(self, clinic_id):
        self.clinic_id = clinic_id
        self.clinic_settings = self._get_clinic_settings_from_database()
        
    def get_referral_data(self, triage_class, interval):
        """Returns historic referral data to use as a start for running ML predictions.

        Parameters:
            `start_date` (str): The start date for predictions.
            `historic_data_year` (str): The year of historic data to query data from.
            `length` (int): The number of days to retrieve historic data for.
        Returns:
            A list of historic referral datapoints.
        """

        triage_class_data = list(filter(lambda c: c['severity'] == triage_class, self.clinic_settings))[0]
        triage_class_duration_days = triage_class_data['duration'] * 7
        
        # Calculate the start and end dates for data retrieval.

        # Establish database connection
        db = DataBase(self.DATABASE_DATA)

        # Query for referral data from previous year
        rows = db.select("SELECT CAST(historicdata.date_received AS VARCHAR), \
                                 CAST(historicdata.date_seen AS VARCHAR) \
                           FROM triagedata.historicdata \
                           WHERE historicdata.date_received >= '%(start_date)s'::date \
                                 AND historicdata.date_received < '%(end_date)s'::date \
                                 AND (historicdata.severity = %(triage_class)s OR \
                                     (historicdata.severity IS NULL AND \
                                      historicdata.date_seen - historicdata.date_received <= %(duration)s))" %
                         {
                             'start_date': interval[0],
                             'end_date': interval[1],
                             'triage_class': triage_class,
                             'duration': triage_class_duration_days
                         })

        # Return results
        return [(self.clinic_id, triage_class) + row for row in rows]
    
    def get_clinic_settings(self):
        return self.clinic_settings

    def _get_clinic_settings_from_database(self):
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
                proportion (float) % of patients within the triage class that should be seen within the duration.
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
                          WHERE clinic_id=%(clinic_id)s" % {'clinic_id': self.clinic_id})

        if len(rows) == 0:
            raise RuntimeError('Could not retrieve clinic settings for clinic-id: %s', self.clinic_id)

        # Return data
        return [dict(zip(keys, values)) for values in rows]
