"""
The ClinicData is used to retrieve historic referral data and triage classes from the database.
"""

# External dependencies.
from api.common.database_interaction import DataBase
from api.common.config import database_config


class ClinicData:
    """
    ClinicData is a class to retrieve historic referral data and triage classes from the database module.
    Usage:
        To create a new ClinicData object, create it with `ClinicData(clinic_id)` where
        those values are:
        ```
        {
            'clinic_id' (int) The ID value of the clinic for which data is needed.
        }
        ```
    """

    # Database connection information
    DATABASE_DATA = {
        'user': 'clinic_data',
        'password': 'password',
        'database': database_config['database'],
        'host': database_config['host'],
        'port': database_config['port']
    }
    """
    This is the database connection information used by ClinicData to connect to the database.
    See `api.common.database_interaction.DataBase` for configuration details and required arguments.
    """

    # Constructor
    def __init__(self, clinic_id):
        self.clinic_id = clinic_id
        self.clinic_settings = self._get_clinic_settings_from_database()

    def get_referral_data(self, triage_class, interval):
        """Returns historic referral data to use as a start for running ML predictions.
        Parameters:
            `triage_class` (int): The triage class severity level.
            `interval` (tuple): A tuple with a start and end date.
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
        """Returns clinic settings (triage classes).
        Returns:
            A list of dictionaries containing triage class information. (See _get_clinic_settings_from_database)
        """
        return self.clinic_settings

    def _get_clinic_settings_from_database(self):
        """
        Retrieves clinic triage class settings for the given clinic.
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

    def update_triage_class(self, triage_class):
        """
        Creates or updates the respective triage class within the clinic.

        Args:
            triage_class (dict): The desired new or updated triage class.
        """

        # Establish database connection
        db = DataBase(self.DATABASE_DATA)
        # Insert or update information
        db.insert("INSERT INTO triagedata.triageclasses (clinic_id, severity, name, duration, proportion) \
                    VALUES(%(clinic_id)s, \
                        %(severity)s, \
                        '%(name)s', \
                        %(duration)s, \
                        %(proportion)s) \
                    ON CONFLICT ON CONSTRAINT pk DO UPDATE \
                        SET name = '%(name)s', \
                            duration = %(duration)s, \
                            proportion = %(proportion)s" %
                  {
                      'clinic_id': triage_class['clinic_id'],
                      'severity': triage_class['severity'],
                      'name': triage_class['name'],
                      'duration': triage_class['duration'],
                      'proportion': triage_class['proportion']
                  })
