"""
This module handles testing for the Upload class.
"""

import io
import os
import uuid
import psycopg2

import pytest
from api.resources.upload import PastAppointments, Model
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
        self.upload_storage_path = './test-upload-storage/'

    @staticmethod
    def _write_file_at_path_with_contents(file_path, contents):
        """
        Create a sample file with some contents for testing purposes.
        """
        with open(file_path, 'w') as f:
            f.write(contents)

    def test_save_model_file_path_to_db_success(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that the operation returns the expected result from the db.
        """
        id = 5
        mocker.patch('api.common.database_interaction.DataBase.insert', return_value=id)

        assert self.model.save_model_file_path_to_db('sample/file/path', 1, 1, 0.95, False) == id

    def test_save_model_file_path_to_db_database_error(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests a database error when saving a model file path.
        """
        mocker.patch('api.common.database_interaction.DataBase.insert', side_effect=psycopg2.ProgrammingError)

        with pytest.raises(psycopg2.ProgrammingError):
            self.model.save_model_file_path_to_db('sample/file/path', 1, 1, 0.95, False)

    def test_save_model_file_path_to_db_error(self):
        pass

    def test_save_weight_file_locally_without_existing_dir(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that a weights file is saved if the directory does not already exist.
        """
        # Test setup
        files_dir = "./testing-files/"
        file_contents = b"sample contents"
        clinic_id, severity = 1, 1
        mock_uuid = mocker.patch('uuid.uuid4', return_value=uuid.UUID("6b8873dc-ac4a-4ac0-8f16-28af79761008"))
        file_name = mock_uuid().hex
        mocker.patch('api.resources.upload.FILE_STORAGE_PATH', files_dir)
        data_file = FileStorage(io.BytesIO(file_contents), filename="test.h5")
        # Testing
        self.model.save_weight_file_locally(data_file, clinic_id, severity)
        assert os.path.exists('%s' % files_dir)
        assert os.path.exists('%s%s' % (files_dir, clinic_id))
        assert os.path.exists('%s%s/%s' % (files_dir, clinic_id, severity))
        assert os.path.exists('%s%s/%s/%s.h5' % (files_dir, clinic_id, severity, file_name))
        with open('%s%s/%s/%s.h5' % (files_dir, clinic_id, severity, file_name), 'r') as f:
            assert f.read() == file_contents.decode()
        # Test clean up
        os.remove('%s%s/%s/%s.h5' % (files_dir, clinic_id, severity, file_name))
        os.rmdir('%s%s/%s' % (files_dir, clinic_id, severity))
        os.rmdir('%s%s' % (files_dir, clinic_id))
        os.rmdir('%s' % files_dir)

    def test_save_weight_file_locally_with_existing_dir(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that a weights file is saved if the directory already exists.
        """
        # Test setup
        files_dir = "./testing-files/"
        file_contents = b"sample contents"
        clinic_id, severity = 1, 1
        os.makedirs('%s%s/%s' % (files_dir, clinic_id, severity), exist_ok=False)
        mock_uuid = mocker.patch('uuid.uuid4', return_value=uuid.UUID("6b8873dc-ac4a-4ac0-8f16-28af79761008"))
        file_name = mock_uuid().hex
        mocker.patch('api.resources.upload.FILE_STORAGE_PATH', files_dir)
        data_file = FileStorage(io.BytesIO(file_contents), filename="test.h5")
        # Testing
        self.model.save_weight_file_locally(data_file, clinic_id, severity)
        assert os.path.exists('%s' % files_dir)
        assert os.path.exists('%s%s' % (files_dir, clinic_id))
        assert os.path.exists('%s%s/%s' % (files_dir, clinic_id, severity))
        assert os.path.exists('%s%s/%s/%s.h5' % (files_dir, clinic_id, severity, file_name))
        with open('%s%s/%s/%s.h5' % (files_dir, clinic_id, severity, file_name), 'r') as f:
            assert f.read() == file_contents.decode()
        # Test clean up
        os.remove('%s%s/%s/%s.h5' % (files_dir, clinic_id, severity, file_name))
        os.rmdir('%s%s/%s' % (files_dir, clinic_id, severity))
        os.rmdir('%s%s' % (files_dir, clinic_id))
        os.rmdir('%s' % files_dir)

    def test_save_weight_file_locally_with_existing_dir_and_contents(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that a weights file is saved if the directory already exists with contents and the contents of
                      the other file remain unchanged. (prevent a sideeffect)
        """
        # Test setup
        files_dir = "./testing-files/"
        file_contents = b"sample contents"
        other_contents = 'other stuff'
        clinic_id, severity = 1, 1
        other_file_full_path = '%s%s/%s/other.txt' % (files_dir, clinic_id, severity)
        os.makedirs('%s%s/%s' % (files_dir, clinic_id, severity), exist_ok=False)
        self._write_file_at_path_with_contents(other_file_full_path, other_contents)
        mock_uuid = mocker.patch('uuid.uuid4', return_value=uuid.UUID("6b8873dc-ac4a-4ac0-8f16-28af79761008"))
        file_name = mock_uuid().hex
        mocker.patch('api.resources.upload.FILE_STORAGE_PATH', files_dir)
        data_file = FileStorage(io.BytesIO(file_contents), filename="test.h5")
        # Testing
        self.model.save_weight_file_locally(data_file, clinic_id, severity)
        assert os.path.exists('%s' % files_dir)
        assert os.path.exists('%s%s' % (files_dir, clinic_id))
        assert os.path.exists('%s%s/%s' % (files_dir, clinic_id, severity))
        assert os.path.exists('%s%s/%s/%s.h5' % (files_dir, clinic_id, severity, file_name))
        with open('%s%s/%s/%s.h5' % (files_dir, clinic_id, severity, file_name), 'r') as f:
            assert f.read() == file_contents.decode()
        with open(other_file_full_path, 'r') as f:
            assert f.read() == other_contents
        # Test clean up
        os.remove('%s%s/%s/%s.h5' % (files_dir, clinic_id, severity, file_name))
        os.remove(other_file_full_path)
        os.rmdir('%s%s/%s' % (files_dir, clinic_id, severity))
        os.rmdir('%s%s' % (files_dir, clinic_id))
        os.rmdir('%s' % files_dir)

    def test_create_directory_if_not_exists(self):
        """
        Test Type: Unit
        Test Purpose: Tests that a directory is made if it doesn't already exist.
        """
        test_dir = './testing-dir'
        self.model.create_directory_if_not_exists(test_dir)
        assert os.path.exists('./testing-dir')
        # Test clean up
        os.rmdir(test_dir)

    def test_create_directory_if_exists(self):
        """
        Test Type: Unit
        Test Purpose: Tests that a directory is made if it doesn't already exist.
        """
        # Test setup
        test_dir = './testing-dir'
        os.makedirs(test_dir, exist_ok=False)
        # Testing
        self.model.create_directory_if_not_exists(test_dir)
        assert os.path.exists('./testing-dir')
        # Test clean up
        os.rmdir(test_dir)

    def test_create_directory_if_exists_with_contents(self):
        """
        Test Type: Unit
        Test Purpose: Tests that a directory is made if it already exists with contents.
        """
        # Test setup
        test_dir = './testing-dir'
        os.makedirs(test_dir, exist_ok=False)
        # Testing
        self.model.create_directory_if_not_exists(test_dir)
        assert os.path.exists('./testing-dir')
        # Test clean up
        os.rmdir(test_dir)

    def test_create_directory_if_exists_without_modifying_existing_contents(self):
        """
        Test Type: Unit
        Test Purpose: Tests that a directory is made if it already exists with contents and
                      those contents are unchanged.
        """
        # Test setup
        test_dir = './testing-dir'
        test_file = './testing-dir/test-file'
        sample_contents = 'sample contents'
        os.makedirs(test_dir, exist_ok=False)
        self._write_file_at_path_with_contents(test_file, sample_contents)
        # Testing
        self.model.create_directory_if_not_exists(test_dir)
        assert os.path.exists('./testing-dir')
        assert os.path.exists(test_file)
        with open(test_file, 'r') as f:
            assert f.read() == sample_contents
        # Test clean up
        os.remove(test_file)
        os.rmdir(test_dir)
