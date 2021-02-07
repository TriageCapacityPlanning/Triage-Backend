import pytest
from api.resources.models import Models
from api.triage_api import create_app
import json


class TestModels:
    def setup_class(self):
        self.test_client = create_app().test_client()

    def test_get_missing_inputs(self):
        input_mock = {}
        response = self.test_client.get('/models', query_string=input_mock)

        assert response.status_code == 422

    def test_get_incorrect_input_type(self):
        input_mock = {'clinic-id': '"1"'}
        response = self.test_client.get('/models', query_string=input_mock)

        assert response.status_code == 422

    def test_get_triage_models_success_singleton(self, mocker):
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
        response = self.test_client.get('/models', query_string=input_mock)

        assert response.status_code == 200
        assert json.loads(response.data)['models'] == triage_models_mock

    def test_get_triage_models_success_multiple(self, mocker):
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
        response = self.test_client.get('/models', query_string=input_mock)

        assert response.status_code == 200
        assert json.loads(response.data)['models'] == triage_models_mock

    def test_patch_missing_inputs(self):
        input_mock = {}
        response = self.test_client.patch('/models', query_string=input_mock)

        assert response.status_code == 422

    def test_patch_incorrect_input_type_clinic_id(self):
        input_mock = {'clinic-id': '"1"', 'model-id': 1}
        response = self.test_client.patch('/models', query_string=input_mock)

        assert response.status_code == 422

    def test_patch_incorrect_input_type_model_id(self):
        input_mock = {'clinic-id': 1, 'model-id': '"1"'}
        response = self.test_client.patch('/models', query_string=input_mock)

        assert response.status_code == 422

    def test_patch_triage_classes_success_singleton(self, mocker):
        mocker.patch(
            'api.resources.models.Models.set_active_model')
        model_id = 1
        input_mock = {'clinic-id': 1, 'model-id': model_id}
        response = self.test_client.patch('/models', query_string=input_mock)
        assert response.status_code == 200
        assert json.loads(response.data)['active_model'] == model_id


class TestModelsUnit:
    def setup_class(self):
        self.models = Models()

    def test_get_triage_models_database_error(self, mocker):
        mocker.patch('api.common.database_interaction.DataBase.select',
                     side_effect=RuntimeError('Database error'))

        with pytest.raises(RuntimeError):
            self.models.get_clinic_models(3)

    def test_get_triage_models_empty_data_error(self, mocker):
        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=[])

        with pytest.raises(RuntimeError):
            self.models.get_clinic_models(3)

    def test_get_triage_models_success_singleton(self, mocker):
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
        mocker.patch('api.common.database_interaction.DataBase.update',
                     side_effect=RuntimeError('Database error'))

        with pytest.raises(RuntimeError):
            self.models.set_active_model(3, 1)

    def test_set_active_triage_model_database_success(self, mocker):
        mocker.patch('api.common.database_interaction.DataBase.update')

        self.models.set_active_model(3, 1)
