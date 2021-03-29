"""
This module handles all required interaction with the `/auth` endpoint
"""

# External dependencies
from flask_restful import Resource
from flask import request
from webargs.flaskparser import parser
from webargs import fields
import ast
import json
import jwt
import datetime
import hashlib
import os

# Internal dependencies
from api.common.database_interaction import DataBase
from api.common.config import database_config

SECRET_KEY = os.environ['API_SECRET']

class Auth(Resource):
    """
    The `Auth` class handles all of the requests relative to authenticating a user for the API.
    """

    DATABASE_DATA = {
        'user': 'auth_handler',
        'password': 'password',
        'database': database_config['database'],
        'host': database_config['host'],
        'port': database_config['port']
    }
    """
    This is the database connection information used by Auth to connect to the database.
    See `api.common.database_interaction.DataBase` for configuration details and required arguments.
    """

    # API input schema
    arg_schema_post = {
        "username": fields.Str(required=True),
        "password": fields.Str(required=True)
    }

    """
    The required schema to handle a post request (authenticate a user and generate a token)

    Args:
        username (str): The user's username.
        password (str): The user's password.
    """

    def post(self):
        """
        Handles a post request for the auth endpoints.
        Returns a generated token and clinic_id of the user if successfully authenticated.

        Args:
            Requires api body arguments, see `Auth.arg_schema_post`, in the post request

        Returns:
            A dictionary with
            ```
            {
                token (str) The user's generated JWT.
                clinic_id (int) The clinic id the user is associated with.
                admin (bool) The user's admin status.
            }
            ```
        """
        # Validate input arguments.
        args = parser.parse(self.arg_schema_post, request, location='json')
        user_clinic, admin = self._validate_user(args['username'], args['password'])
        return json.dumps({'token': self._generate_token(args['username'], user_clinic), 'clinic_id': user_clinic, 'admin': admin })

    def _validate_user(self, username, password):
        db = DataBase(self.DATABASE_DATA)
        query = "SELECT clinic_id, admin, password, salt FROM triagedata.users "
        query += "WHERE username='%s' " % username

        result = db.select(query)

        if len(result) > 0:
            user_data = [user for user in result if user[2] == hashlib.sha512((password + user[3]).encode()).hexdigest()]
            if len(user_data) > 0:
                return result[0][0], result[0][1]
            else:
                    raise RuntimeError('Invalid User Credentials')
        else:
            raise RuntimeError('Invalid User Credentials')

    def _generate_token(self, username, user_clinic):
        return str(jwt.encode({
                'user': username,
                'clinic': user_clinic,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
            },
            SECRET_KEY, algorithm="HS256"))
