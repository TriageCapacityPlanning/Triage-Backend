import pytest
from api.resources.update_triage_classes import UpdateTriageClasses
from api.triage_api import create_app
import json


class TestUpdateTriageClassesAPI:
    def setup_class(self):
        self.test_client = create_app().test_client()

    def test_get_missing_inputs(self):
        input_mock = {}
        response = self.test_client.get('/classes', query_string=input_mock)

        assert response.status_code == 422

    def test_get_incorrect_input_type(self):
        input_mock = {'clinic-id': '"1"'}
        response = self.test_client.get('/classes', query_string=input_mock)

        assert response.status_code == 422

    def test_get_triage_classes_success_singleton(self, mocker):
        triage_classes_mock = [
            {
                'clinic_id': 3,
                'severity': 1,
                'name': 'Urgent',
                'duration': 2,
                'proportion': 0.8
            }
        ]
        mocker.patch('api.resources.update_triage_classes.UpdateTriageClasses.get_triage_classes',
                     return_value=triage_classes_mock)

        input_mock = {'clinic-id': 1}
        response = self.test_client.get('/classes', query_string=input_mock)

        assert response.status_code == 200
        assert json.loads(response.data)['classes'] == triage_classes_mock

    def test_get_triage_classes_success_multiple(self, mocker):
        triage_classes_mock = [
            {
                'clinic_id': 3,
                'severity': 1,
                'name': 'Urgent',
                'duration': 2,
                'proportion': 0.8
            },
            {
                'clinic_id': 3,
                'severity': 2,
                'name': 'Semi-Urgent',
                'duration': 4,
                'proportion': 0.7
            },
            {
                'clinic_id': 3,
                'severity': 3,
                'name': 'Standard',
                'duration': 6,
                'proportion': 0.6
            }
        ]
        mocker.patch('api.resources.update_triage_classes.UpdateTriageClasses.get_triage_classes',
                     return_value=triage_classes_mock)

        input_mock = {'clinic-id': 1}
        response = self.test_client.get('/classes', query_string=input_mock)

        assert response.status_code == 200
        assert json.loads(response.data)['classes'] == triage_classes_mock

    def test_put_missing_inputs(self):
        input_mock = {}
        response = self.test_client.put('/classes', json=(input_mock))

        assert response.status_code == 422

    def test_put_incorrect_input_type(self):
        input_mock = {'triage-class': '"1"'}
        response = self.test_client.put('/classes', json=(input_mock))

        assert response.status_code == 422

    def test_put_triage_classes_success_singleton(self, mocker):
        mocker.patch('api.resources.update_triage_classes.UpdateTriageClasses.update_triage_class')

        triage_class_mock = {
            'clinic-id': 1,
            'severity': 1,
            'name': 'Urgent',
            'duration': 2,
            'proportion': 0.8
        }
        input_mock = {
            'triage-class': triage_class_mock
        }
        response = self.test_client.put('/classes', json=(input_mock))
        assert response.status_code == 200
        assert json.loads(response.data)['updated'] == triage_class_mock


class TestUpdateTriageClassesUnit:
    def setup_class(self):
        self.update_triage_classes = UpdateTriageClasses()

    def test_get_triage_classes_database_error(self, mocker):
        mocker.patch('api.common.database_interaction.DataBase.select',
                     side_effect=RuntimeError('Database error'))

        with pytest.raises(RuntimeError):
            self.update_triage_classes.get_triage_classes(3)

    def test_get_triage_classes_empty_data_error(self, mocker):
        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=[])

        with pytest.raises(RuntimeError):
            self.update_triage_classes.get_triage_classes(3)

    def test_get_triage_classes_success_singleton(self, mocker):
        database_response_mock = [[3, 1, 'Urgent', 2, 0.8]]
        result_expected = [
            {
                'clinic_id': 3,
                'severity': 1,
                'name': 'Urgent',
                'duration': 2,
                'proportion': 0.8
            }
        ]

        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=database_response_mock)

        assert self.update_triage_classes.get_triage_classes(
            3) == result_expected

    def test_get_triage_classes_success_multiple(self, mocker):
        database_response_mock = [
            [3, 1, 'Urgent', 2, 0.8],
            [3, 2, 'Semi-Urgent', 4, 0.7],
            [3, 3, 'Standard', 6, 0.6],
        ]

        result_expected = [
            {
                'clinic_id': 3,
                'severity': 1,
                'name': 'Urgent',
                'duration': 2,
                'proportion': 0.8
            },
            {
                'clinic_id': 3,
                'severity': 2,
                'name': 'Semi-Urgent',
                'duration': 4,
                'proportion': 0.7
            },
            {
                'clinic_id': 3,
                'severity': 3,
                'name': 'Standard',
                'duration': 6,
                'proportion': 0.6
            }
        ]
        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=database_response_mock)

        assert self.update_triage_classes.get_triage_classes(
            3) == result_expected

    def test_update_triage_class_database_error(self, mocker):
        triage_class_input = {
            'clinic-id': 3,
            'severity': 1,
            'name': 'Urgent',
            'duration': 2,
            'proportion': 0.8
        }

        mocker.patch('api.common.database_interaction.DataBase.insert',
                     side_effect=RuntimeError('Database error'))

        with pytest.raises(RuntimeError):
            self.update_triage_classes.update_triage_class(triage_class_input)

    def test_update_triage_class_database_success(self, mocker):
        triage_class_input = {
            'clinic-id': 3,
            'severity': 1,
            'name': 'Urgent',
            'duration': 2,
            'proportion': 0.8
        }

        mocker.patch('api.common.database_interaction.DataBase.insert')

        try:
            self.update_triage_classes.update_triage_class(triage_class_input)
        except exception:
            raise pytest.fail('Did raise %s', exception)
