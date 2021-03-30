"""
This module handles testing for the Upload class.
"""

import io

import pytest
from api.resources.upload import PastAppointments, Model, FileError
from api.triage_api import create_app
from api.common.config import VERSION_PREFIX
from api.tests.common import generate_token
from werkzeug.datastructures import FileStorage


class TestUploadPastAppointmentsAPI:
    """
    The `TestUploadPastAppointmentsAPI` class contains acceptance tests for /upload/past-appointments
    API functions.
    """

    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """
        self.test_client = create_app().test_client()
        self.token = generate_token('username', 1)
        self.endpoint = VERSION_PREFIX + '/upload/past-appointments'

    def test_put_missing_inputs(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-7, DAT-1, DAT-4
        """

        input_mock = {}
        response = self.test_client.put(self.endpoint, headers={'token': self.token}, data=input_mock)

        assert response.status_code == 422

    def test_put_incorrect_input_type_clinic_id(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-7, DAT-1, DAT-4
        """
        upload_file_mock = FileStorage(io.BytesIO(b"file contents"), filename="data.txt", content_type="text/csv")
        input_mock = {
            'clinic_id': '"1"',
            'upload_data': upload_file_mock
        }
        response = self.test_client.put(self.endpoint, headers={'token': self.token}, data=input_mock)

        assert response.status_code == 422

    def test_put_incorrect_input_type_file(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-7, DAT-1, DAT-4
        """
        upload_file_mock = FileStorage(io.BytesIO(b"file contents"), filename="data.txt", content_type="text/text")
        input_mock = {
            'clinic_id': 1,
            'upload_data': upload_file_mock
        }

        response = self.test_client.put(self.endpoint, headers={'token': self.token}, data=input_mock)

        assert response.status_code == 422

    def test_upload_success(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-7, DAT-1, DAT-4
        """
        mocker.patch('api.resources.upload.PastAppointments.upload_csv_data')
        upload_file_mock = FileStorage(io.BytesIO(b"file contents"), filename="data.csv", content_type="text/csv")
        input_mock = {
            'clinic_id': 1,
            'upload_data': upload_file_mock
        }

        response = self.test_client.put(self.endpoint, headers={'token': self.token}, data=input_mock)

        assert response.status_code == 200

    def test_upload_requires_header_with_token(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-7, DAT-1, DAT-4
        """
        mocker.patch('api.resources.upload.PastAppointments.upload_csv_data')
        upload_file_mock = FileStorage(io.BytesIO(b"file contents"), filename="data.csv", content_type="text/csv")
        input_mock = {
            'clinic_id': 1,
            'upload_data': upload_file_mock
        }
        response = self.test_client.put(self.endpoint, data=input_mock)
        assert response.status_code == 401

    def test_upload_requires_valid_token(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-7, DAT-1, DAT-4
        """
        mocker.patch('api.resources.upload.PastAppointments.upload_csv_data')
        upload_file_mock = FileStorage(io.BytesIO(b"file contents"), filename="data.csv", content_type="text/csv")
        input_mock = {
            'clinic_id': 1,
            'upload_data': upload_file_mock
        }
        response = self.test_client.put(self.endpoint, headers={'token': "not_valid_token"}, data=input_mock)
        assert response.status_code == 401


class TestUploadModelAPI:
    """
    The `TestUploadModelAPI` class contains acceptance tests for /upload/model API functions.
    """

    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """
        self.test_client = create_app().test_client()
        self.token = generate_token('username', 1)
        self.endpoint = VERSION_PREFIX + '/upload/model'

    def test_put_missing_inputs(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        input_mock = {}
        response = self.test_client.post(self.endpoint, headers={'token': self.token}, data=input_mock)

        assert response.status_code == 422

    def test_put_incorrect_input_type_clinic_id(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        upload_file_mock = FileStorage(io.BytesIO(b"weights file contents"), filename="w.h5")
        input_mock = {
            'clinic_id': '"1"',
            'model_weights': upload_file_mock,
            'severity': 1,
            'accuracy': 0.95,
            'make_in_use': False,
        }
        response = self.test_client.post(self.endpoint, headers={'token': self.token}, data=input_mock)
        assert response.status_code == 422

    def test_put_incorrect_input_type_file(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        input_mock = {
            'clinic_id': '"1"',
            'model_weights': "not_a_file",
            'severity': 1,
            'accuracy': 0.95,
            'make_in_use': False,
        }
        response = self.test_client.post(self.endpoint, headers={'token': self.token}, data=input_mock)
        assert response.status_code == 422

    def test_put_incorrect_input_type_severity(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        upload_file_mock = FileStorage(io.BytesIO(b"weights file contents"), filename="w.h5")
        input_mock = {
            'clinic_id': 1,
            'model_weights': upload_file_mock,
            'severity': '"1"',
            'accuracy': 0.95,
            'make_in_use': False,
        }
        response = self.test_client.post(self.endpoint, headers={'token': self.token}, data=input_mock)
        assert response.status_code == 422

    def test_put_incorrect_input_type_accuracy(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        upload_file_mock = FileStorage(io.BytesIO(b"weights file contents"), filename="w.h5")
        input_mock = {
            'clinic_id': 1,
            'model_weights': upload_file_mock,
            'severity': 1,
            'accuracy': '"0.95"',
            'make_in_use': False,
        }
        response = self.test_client.post(self.endpoint, headers={'token': self.token}, data=input_mock)
        assert response.status_code == 422

    def test_put_incorrect_input_type_make_in_use(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        upload_file_mock = FileStorage(io.BytesIO(b"weights file contents"), filename="w.h5")
        input_mock = {
            'clinic_id': 1,
            'model_weights': upload_file_mock,
            'severity': 1,
            'accuracy': 0.95,
            'make_in_use': '"yes"',
        }
        response = self.test_client.post(self.endpoint, headers={'token': self.token}, data=input_mock)
        assert response.status_code == 422

    def test_upload_success_not_make_active(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        mocker.patch('api.resources.upload.Model.save_weight_file_locally')
        mocker.patch('api.resources.upload.Model.save_model_file_path_to_db')
        upload_file_mock = FileStorage(io.BytesIO(b"weights file contents"), filename="w.h5")
        input_mock = {
            'clinic_id': 1,
            'model_weights': upload_file_mock,
            'severity': 1,
            'accuracy': 0.95,
            'make_in_use': False,
        }

        response = self.test_client.post(self.endpoint, headers={'token': self.token}, data=input_mock)

        assert response.status_code == 200

    def test_upload_success_make_active(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        mocker.patch('api.resources.upload.Model.save_weight_file_locally')
        mocker.patch('api.resources.upload.Model.save_model_file_path_to_db')
        mocker.patch('api.resources.upload.Models.set_active_model')
        upload_file_mock = FileStorage(io.BytesIO(b"weights file contents"), filename="w.h5")
        input_mock = {
            'clinic_id': 1,
            'model_weights': upload_file_mock,
            'severity': 1,
            'accuracy': 0.95,
            'make_in_use': True,
        }

        response = self.test_client.post(self.endpoint, headers={'token': self.token}, data=input_mock)

        assert response.status_code == 200

    def test_upload_requires_header_with_token(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        upload_file_mock = FileStorage(io.BytesIO(b"weights file contents"), filename="w.h5")
        input_mock = {
            'clinic_id': 1,
            'model_weights': upload_file_mock,
            'severity': 1,
            'accuracy': 0.95,
            'make_in_use': False,
        }
        response = self.test_client.post(self.endpoint, data=input_mock)
        assert response.status_code == 401

    def test_upload_requires_valid_token(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        upload_file_mock = FileStorage(io.BytesIO(b"weights file contents"), filename="w.h5")
        input_mock = {
            'clinic_id': 1,
            'model_weights': upload_file_mock,
            'severity': 1,
            'accuracy': 0.95,
            'make_in_use': False,
        }
        response = self.test_client.post(self.endpoint, headers={'token': "not_valid_token"}, data=input_mock)
        assert response.status_code == 401


class TestPastAppointmentsUnit:
    """
    The `TestPastAppointmentsUnit` class contains unit tests for uploading past appointments functions.
    """

    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """
        self.pastappointments = PastAppointments()

    def test_upload_csv_data_database_error(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that an error is thrown if a the database connection fails.
        """
        upload_file_mock = FileStorage(io.BytesIO(b"file contents"), filename="data.csv", content_type="text/csv")
        mocker.patch('api.common.database_interaction.DataBase.insert_data_from_file',
                     side_effect=RuntimeError('Database error'))

        with pytest.raises(RuntimeError):
            self.pastappointments.upload_csv_data(upload_file_mock)

    def test_upload_csv_data_file_error(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that an error is thrown if a the file upload fails.
        """
        upload_file_mock = FileStorage(io.BytesIO(b"file contents"), filename="data.csv", content_type="text/csv")
        mocker.patch('api.common.database_interaction.DataBase.insert_data_from_file',
                     side_effect=RuntimeError('File error'))

        with pytest.raises(RuntimeError):
            self.pastappointments.upload_csv_data(upload_file_mock)

    def test_upload_csv_data_successful(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that a successful file upload.
        """
        upload_file_mock = FileStorage(io.BytesIO(b"file contents"), filename="data.csv", content_type="text/csv")
        mocker.patch('api.common.database_interaction.DataBase.insert_data_from_file')

        assert self.pastappointments.upload_csv_data(upload_file_mock) is None


class TestModelUnit:
    """
    The `TestModelUnit` class contains unit tests for uploading models to the server functions.
    """

    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """
        self.model = Model()
