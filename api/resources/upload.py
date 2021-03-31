"""
This module handles all required interaction with the `/upload` endpoints
"""
from api.common.exceptions import FileError
from flask import request
from webargs.flaskparser import parser
from webargs import fields
import os
import uuid


# Internal dependencies
from api.resources.AuthResource import AuthResource
from api.common.database_interaction import DataBase
from api.resources.models import Models
from api.common.config import database_config

FILE_STORAGE_PATH = 'uploads/'


class PastAppointments(AuthResource):
    """
    The `PastAppointments` class handles all of the requests relative to historic
    triage data for the API.
    """
    DATABASE_DATA = {
        'user': 'historic_data_handler',
        'password': 'password',
        'database': database_config['database'],
        'host': database_config['host'],
        'port': database_config['port']
    }
    """
    This is the database connection information used by PastAppointments to connect to the database.
    See `api.common.database_interaction.DataBase` for configuration details and required arguments.
    """

    arg_schema_put = {
        'clinic_id': fields.Int(required=True),
        'upload_data': fields.Field()
    }
    """
    The required schema to handle a put request

    Args:
        clinic_id (int): The id of the clinic uploading data
    """

    def put(self):
        """
        Handles a put request for the upload past appointments (historic data) endpoint.

        Args:
            Requires api body arguments, see `PastAppointments.arg_schema_put`, in the put request
        """
        parser.parse(self.arg_schema_put, request, location='json_or_form')
        if not request.files.get('upload_data'):
            raise FileError("Missing upload file.")
        # Figure out how to validate inputs
        mime_type = request.files.get('upload_data').mimetype
        if mime_type == 'text/csv':
            self.upload_csv_data(request.files.get('upload_data'))
        else:
            raise FileError("Bad upload file type received.")
        return {'status': 200}

    def upload_csv_data(self, upload_file):
        """
        Saves The information from a csv file directly into the database.

        The file is not expected to contain headers.
        Expected rows contain: 'clinic_id', 'severity', 'date_received', 'date_seen'

        Args:
            upload_file (file, csv): The csv file to import into the database.
        """
        db = DataBase(self.DATABASE_DATA)
        db.insert_data_from_file(
                'triagedata.historicdata',
                ('clinic_id', 'severity', 'date_received', 'date_seen'),
                upload_file,
                ','
            )


class Model(AuthResource):
    """
    The `Model` class handles all of the requests relative to new model data uploads for the API.
    """
    DATABASE_DATA = {
        'user': 'model_handler',
        'password': 'password',
        'database': database_config['database'],
        'host': database_config['host'],
        'port': database_config['port']
    }
    """
    This is the database connection information used by PastAppointments to connect to the database.
    See `api.common.database_interaction.DataBase` for configuration details and required arguments.
    """

    arg_schema_post = {
        'clinic_id': fields.Int(required=True),
        'model_weights': fields.Field(),
        'severity': fields.Int(required=True),
        'accuracy': fields.Float(required=True),
        'make_in_use': fields.Boolean(),
    }
    """
    The required schema to handle a post request

    Args:
        clinic_id (int): The id of the clinic uploading data
        model_weights (byte array): The model weights data (file)
        accuracy (float): The accuracy for the given model
        make_in_use (bool): (Optional) Make the model in use for the clinic
    """

    def post(self):
        """
        Handles a post request for the upload models endpoint.

        Args:
            Requires api body arguments, see `Model.arg_schema_post`, in the post request
        """
        args = parser.parse(self.arg_schema_post, request, location='json_or_form')
        data_file = request.files['model_weights']
        if not data_file:
            raise FileError("Missing upload file.")
        file_path = self.save_weight_file_locally(data_file, args['clinic_id'], args['severity'])
        model_id = self.save_model_file_path_to_db(file_path, args['clinic_id'], args['severity'], args['accuracy'], False)
        if 'make_in_use' in args and args['make_in_use']:
            Models().set_active_model(args['clinic_id'], model_id)

    def save_model_file_path_to_db(self, file_path, clinic_id, severity, accuracy, in_use):
        """
        Saves The information for a weights file to the database.

        Args:
            file_path (str): The file path to the actual weights file from the backend.
            clinic_id (int, str): The clinic id the weights file was generated for.
            severity (int, str): The severity classification the weights file was generated for.
            accuracy (float): The accuracy of the weights file.
            in_use (bool): Set the weight the the in use file for that clinic id/severity

        Returns:
            The id of the generated row from inserting in the db.
        """
        db = DataBase(self.DATABASE_DATA)
        query = "INSERT INTO triagedata.models (file_path, clinic_id, severity, accuracy, in_use) "
        query += "VALUES ('%s', %s, %s, %s, %s) " % (file_path, clinic_id, severity, accuracy, in_use)
        query += "RETURNING id"
        return db.insert(query, returning=True)

    def save_weight_file_locally(self, data_file, clinic_id, severity):
        """
        Saves a data file under a specified clinic_id and severity subfolder with a randomly generated name

        Args:
            data_file (FileStorage): The file that is being saved. Any open stream with a .save(path) method will work.
            clinic_id (int, str): The clinic id the file was generated for.
            severity (int, str): The severity classification the file was generated for.

        Returns:
            The full file path where the file was saved
        """
        upload_dir = FILE_STORAGE_PATH + "%s/%s" % (clinic_id, severity)
        file_name = uuid.uuid4().hex + '.h5'
        file_path = os.path.join(upload_dir, file_name)
        self.create_directory_if_not_exists(upload_dir)
        data_file.save(file_path)
        return file_path

    @staticmethod
    def create_directory_if_not_exists(directory_path):
        """
        Creates a directory at the provided path if it does not already exist

        Args:
            directory_path (str): The directory that should be created if it does not already exist
        """
        os.makedirs(directory_path, exist_ok=True)
