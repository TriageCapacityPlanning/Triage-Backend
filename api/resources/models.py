"""
This module handles all required interaction with the `/models` endpoints
"""

# External dependencies
from flask import request
from webargs.flaskparser import parser
from webargs import fields


# Internal dependencies
from api.resources.AuthResource import AuthResource
from api.common.database_interaction import DataBase
from api.common.config import database_config


class Models(AuthResource):
    """
    The `Models` class handles all of the requests relative to Models
    for the API.
    """
    DATABASE_DATA = {
        'user': 'model_handler',
        'password': 'password',
        'database': database_config['database'],
        'host': database_config['host'],
        'port': database_config['port']
    }
    """
    This is the database connection information used by Models to connect
    to the database. See `api.common.database_interaction.DataBase`
    for configuration details and required arguments.
    """

    arg_schema_get = {
        'clinic-id': fields.Int(required=True)
    }
    """
    The required schema to handle a get request
    Args:
        clinic-id (int): The id of the clinic being referenced
    """

    arg_schema_patch = {
        'clinic-id': fields.Int(required=True),
        'model-id': fields.Int(required=True)
    }
    """
    The required schema to handle a patch request
    Args:
        clinic-id (int): The id of the clinic being referenced
        model-id (int): The desired new primary model's id
    """

    def get(self):
        """
        Handles a get request for the models endpoints.
        Returns a dictionary with a list of models for an associated clinic.
        Args:
            Requires api query string arguments, see `Models.arg_schema_get`,
            in the get request
        Returns:
            A dictionary with
            `status` (int) The status of the request
            `models` (list): A list of dictionaries representing each model
        """
        # Validate input arguments.
        args = parser.parse(self.arg_schema_get, request,
                            location='querystring')
        # Retrieve clinic models from database
        models = self.get_clinic_models(args['clinic-id'])
        # API Response
        return {'status': 200, 'models': models}

    def patch(self):
        """
        Handles a patch request for the models endpoints.
        Returns a dictionary with an active model.
        Args:
            Requires api query string arguments, see `Models.arg_schema_patch`,
            in the get request
        Returns:
            A dictionary with
            `status` (int) The status of the request
            `active_model` (int): The active model id for the clinic
        """
        # Validate input arguments.
        args = parser.parse(self.arg_schema_patch, request,
                            location='querystring')
        # Update current active model for clinic-id to model-id
        self.set_active_model(args['clinic-id'], args['model-id'])
        # API Response
        return {'status': 200, 'active_model': args['model-id']}

    def set_active_model(self, clinic_id, model_id):
        """
        Sets the active model for the given clinic if the model id exists
        for that clinic.
        Args:
            clinic_id (int): The id of the clinic being referenced
            model_id (int): The desired new primary model's id
        """
        # Establish database connection
        db = DataBase(self.DATABASE_DATA)
        # Update database data
        query = "UPDATE triagedata.models SET in_use = (CASE WHEN id=%s THEN true ELSE false END)" % model_id
        query += "WHERE (SELECT COUNT(*) FROM triagedata.models WHERE id=%s)=1" % model_id
        query += " AND severity=(SELECT severity FROM triagedata.models WHERE id=%s)" % model_id
        query += " AND clinic_id=%s" % clinic_id

        db.update(query)

    def get_clinic_models(self, clinic_id):
        """
        Gets the available models for the given clinic.
        Args:
            clinic_id (int): The id of the clinic being referenced
        Returns:
            list: A list of dictionaries that map the key to the
                  value stored in the database
        """
        # Keys for response
        keys = ['id', 'accuracy', 'created', 'in_use']
        # Establish database connection and get the data
        db = DataBase(self.DATABASE_DATA)
        rows = db.select("SELECT id, accuracy, to_char(created,'DD-MM-YYYY'), in_use \
                           FROM triagedata.models \
                           WHERE clinic_id=%s" % (clinic_id))
        if not rows:
            msg = f'Could not retrieve models for clinic-id: {clinic_id}'
            raise RuntimeError(msg)

        # Return data
        return [dict(zip(keys, values)) for values in rows]
