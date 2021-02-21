"""
This module handles all required interaction with the `/classes` endpoint
"""

# External dependencies
from flask_restful import Resource
from flask import request
from webargs.flaskparser import parser
from webargs import fields

# Internal dependencies
from api.common.database_interaction import DataBase


class UpdateTriageClasses(Resource):
    """
    The `UpdateTriageClasses` class handles all of the requests relative to updating triage class data for the API.
    """

    DATABASE_DATA = {
        'database': 'triage',
        'user': 'triage_class_handler',
        'password': 'password',
        'host': 'db',
        'port': '5432'
    }
    """
    This is the database connection information used by Models to connect to the database.
    See `api.common.database_interaction.DataBase` for configuration details and required arguments.
    """

    arg_schema_get = {
        'clinic_id': fields.Int(required=True)
    }
    """
    The required schema to handle a get request

    Args:
        clinic_id (int): The id of the clinic being referenced
    """

    arg_schema_put = {
        'triage-class': fields.Dict(required=True, keys=fields.Str(), values=fields.Raw())
    }
    """
    The required schema to hangle a patch request

    Args:
        triage-class (int): A dictionary containing a triage classes information including
        ```
        {
            clinic_id (int): The ID of the clinic.
            severity (int): The severity level of the triage class.
            name (str): The name of the triage class.
            duration (int): The time (in weeks) within which a patient in the triage class should be seen.
            proportion (float): The proportion of patients in the triage class that must be seen in a reasonable time.
        }
        ```
    """

    def get(self):
        """
        Handles a get request for the classes endpoints.
        Returns a dictionary with a list of triage classes for an associated clinic.

        Args:
            Requires api query string arguments, see `UpdateTriageClasses.arg_schema_get`, in the get request

        Returns:
            A dictionary with
            `status` (int) The status of the request
            `classes` (list): A list of dictionaries representing each triage class.
        """

        # Validate input arguments.
        args = parser.parse(self.arg_schema_get, request,
                            location='querystring')
        # Retrieve triage classes from database
        triage_classes = self.get_triage_classes(args['clinic_id'])
        # API Response
        return {'status': 200, 'classes': triage_classes}

    def put(self):
        """
        Handles a put request for the classes endpoints.
        Updates or creates a triage class in the database.

        Args:
            Requires api query string arguments, see `UpdateTriageClasses.arg_schema_put`, in the put request

        Returns:
            A dictionary with
            `status` (int) The status of the request
            `updated` (dict): The created or updated class.
        """
        # Validate input arguments
        print(request.json)
        args = parser.parse(self.arg_schema_put, request, location='json')

        # Update triage class in database
        self.update_triage_class(args['triage-class'])

        # API Response
        return {'status': 200, 'updated': args['triage-class']}

    def get_triage_classes(self, clinic_id):
        """
        Gets the available triage classes for the given clinic.

        Args:
            clinic_id (int): The id of the clinic being referenced.

        Returns:
            A list of dictionaries representing the triage classes for the clinic.
        """
        # Keys for response
        keys = ['clinic_id', 'severity', 'name', 'duration', 'proportion']

        # Establish database connection and get the data
        db = DataBase(self.DATABASE_DATA)
        rows = db.select(("SELECT clinic_id, severity, name, duration, proportion \
                        FROM triagedata.triageclasses \
                        WHERE clinic_id=%(clinic_id)s" % {'clinic_id': clinic_id}))

        if len(rows) == 0:
            raise RuntimeError('Could not retrieve clinic settings for clinic_id: %s', clinic_id)

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
