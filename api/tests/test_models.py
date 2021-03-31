import pytest
from api.common.config import VERSION_PREFIX
from api.resources.models import Models
from api.triage_api import create_app
from api.tests.common import generate_token
import json


class TestModelsAPI:
    """
    The `TestModelsAPI` class contains acceptance tests for models API functions.
    """
    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """
        self.test_client = create_app().test_client()
        self.token = generate_token('username', 1)
        self.endpoint = VERSION_PREFIX + '/models'

    def test_get_missing_inputs(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        input_mock = {}
        response = self.test_client.get(self.endpoint, headers={'token': self.token}, query_string=input_mock)

        assert response.status_code == 422

    def test_get_incorrect_input_type(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        input_mock = {'clinic-id': '"1"'}
        response = self.test_client.get(self.endpoint, headers={'token': self.token}, query_string=input_mock)

        assert response.status_code == 422

    def test_get_triage_models_success_singleton(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        triage_models_mock = [
            {
                'id': 1,
                'accuracy': .99,
                'created': '05-05-2020',
                'in_use': 'true'
            }
        ]
        mocker.patch('api.resources.models.Models.get_clinic_models',
                     return_value=triage_models_mock)

        input_mock = {'clinic-id': 3}
        response = self.test_client.get(self.endpoint, headers={'token': self.token}, query_string=input_mock)

        assert response.status_code == 200
        assert json.loads(response.data)['models'] == triage_models_mock

    def test_get_triage_models_success_multiple(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        triage_models_mock = [
            {
                'id': 1,
                'accuracy': .95,
                'created': '05-05-2020',
                'in_use': 'false'
            },
            {
                'id': 2,
                'accuracy': .92,
                'created': '05-06-2020',
                'in_use': 'false'
            },
            {
                'id': 3,
                'accuracy': .99,
                'created': '05-07-2020',
                'in_use': 'true'
            }
        ]
        mocker.patch('api.resources.models.Models.get_clinic_models',
                     return_value=triage_models_mock)

        input_mock = {'clinic-id': 1}
        response = self.test_client.get(self.endpoint, headers={'token': self.token}, query_string=input_mock)

        assert response.status_code == 200
        assert json.loads(response.data)['models'] == triage_models_mock

    def test_get_models_requires_header_with_token(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        mocker.patch('api.resources.models.Models.get_clinic_models')
        model_id = 1
        input_mock = {'clinic-id': 1, 'model-id': model_id}
        response = self.test_client.get(self.endpoint, query_string=input_mock)
        assert response.status_code == 401

    def test_get_models_requires_valid_token(self, mocker):
        mocker.patch('api.resources.models.Models.get_clinic_models')
        model_id = 1
        input_mock = {'clinic-id': 1, 'model-id': model_id}
        response = self.test_client.get(self.endpoint, headers={'token': "not_valid_token"}, query_string=input_mock)
        assert response.status_code == 401

    def test_patch_missing_inputs(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        input_mock = {}
        response = self.test_client.patch(self.endpoint, headers={'token': self.token}, query_string=input_mock)

        assert response.status_code == 422

    def test_patch_incorrect_input_type_clinic_id(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        input_mock = {'clinic-id': '"1"', 'model-id': 1}
        response = self.test_client.patch(self.endpoint, headers={'token': self.token}, query_string=input_mock)

        assert response.status_code == 422

    def test_patch_incorrect_input_type_model_id(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        input_mock = {'clinic-id': 1, 'model-id': '"1"'}
        response = self.test_client.patch(self.endpoint, headers={'token': self.token}, query_string=input_mock)

        assert response.status_code == 422

    def test_patch_models_success_singleton(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        mocker.patch(
            'api.resources.models.Models.set_active_model')
        model_id = 1
        input_mock = {'clinic-id': 1, 'model-id': model_id}
        response = self.test_client.patch(self.endpoint, headers={'token': self.token}, query_string=input_mock)
        assert response.status_code == 200
        assert json.loads(response.data)['active_model'] == model_id

    def test_patch_models_requires_header_with_token(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        mocker.patch('api.resources.models.Models.set_active_model')
        model_id = 1
        input_mock = {'clinic-id': 1, 'model-id': model_id}
        response = self.test_client.patch(self.endpoint, query_string=input_mock)
        assert response.status_code == 401

    def test_patch_models_requires_valid_token(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement
        """
        mocker.patch('api.resources.models.Models.set_active_model')
        model_id = 1
        input_mock = {'clinic-id': 1, 'model-id': model_id}
        response = self.test_client.patch(self.endpoint, headers={'token': "not_valid_token"}, query_string=input_mock)
        assert response.status_code == 401


class TestModelsUnit:
    """
    The `TestModelsUnit` class contains unit tests for models functions.
    """
    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """
        self.models = Models()

    def test_get_triage_models_database_error(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that an error is thrown if a the database connection fails.
        """
        mocker.patch('api.common.database_interaction.DataBase.select',
                     side_effect=RuntimeError('Database error'))

        with pytest.raises(RuntimeError):
            self.models.get_clinic_models(3)

    def test_get_triage_models_empty_data_error(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that an error is thrown if the database returns no rows.
        """
        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=[])

        with pytest.raises(RuntimeError):
            self.models.get_clinic_models(3)

    def test_get_triage_models_success_singleton(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that a singleton is returned if a single tuple was found in the db.
        """
        database_response_mock = [[1, .95, '05-05-2020', 'true']]
        result_expected = [
            {
                'id': 1,
                'accuracy': .95,
                'created': '05-05-2020',
                'in_use': 'true'
            }
        ]

        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=database_response_mock)

        assert self.models.get_clinic_models(3) == result_expected

    def test_get_triage_models_success_multiple(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that multiple rows are returned if multiple tuples are found in the db.
        """
        database_response_mock = [
            [1, .95, '05-05-2020', 'false'],
            [2, .92, '05-06-2020', 'false'],
            [3, .98, '05-07-2020', 'true']
        ]
        result_expected = [
            {
                'id': 1,
                'accuracy': .95,
                'created': '05-05-2020',
                'in_use': 'false'
            },
            {
                'id': 2,
                'accuracy': .92,
                'created': '05-06-2020',
                'in_use': 'false'
            },
            {
                'id': 3,
                'accuracy': .98,
                'created': '05-07-2020',
                'in_use': 'true'
            }
        ]

        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=database_response_mock)

        assert self.models.get_clinic_models(3) == result_expected

    def test_set_active_triage_model_database_error(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that an error is thrown if a the database connection fails.
        """
        mocker.patch('api.common.database_interaction.DataBase.update',
                     side_effect=RuntimeError('Database error'))

        with pytest.raises(RuntimeError):
            self.models.set_active_model(3, 1)

    def test_set_active_triage_model_database_success(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that no error is thrown if a the update is successful.
        """
        mocker.patch('api.common.database_interaction.DataBase.update')

        self.models.set_active_model(3, 1)
