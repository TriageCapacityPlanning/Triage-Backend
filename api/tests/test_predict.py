"""
This module handles testing for the Predict class.
"""

import pytest
import json
from api.resources.predict import Predict
from api.triage_api import create_app

class TestPredictAPI:
    """
    The `TestPredictAPI` class contains acceptance tests for predict API functions.
    """

    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """

        self.test_client = create_app().test_client()

    def test_get_missing_inputs(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-6
        """

        input_mock = {}
        response = self.test_client.get('/predict', query_string=input_mock)

        assert response.status_code == 422

    def test_get_incorrect_input_type(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-6
        """

        input_mock = {
            "clinic-id": '"2"',
            "start-date": '2020-01-01',
            "end-date": '2020-12-31',
            "intervals": [['2020-01-01', '2020-06-01'], ['2020-06-02', '2020-12-31']],
            "confidence": 0.95,
            "num-sim-runs": 1000,
            "waitlist": []
        }
        response = self.test_client.get('/predict', query_string=input_mock)

        assert response.status_code == 422

    def test_get_success(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-6
        """

        input_mock = {
            "clinic-id": 3,
            "start-date": '2020-01-01',
            "end-date": '2020-12-31',
            "intervals": [['2020-01-01', '2020-06-01'], ['2020-06-02', '2020-12-31']],
            "confidence": 0.95,
            "num-sim-runs": 1000,
            "waitlist": []
        }

        predictions_mock = {
            'interval': [
                {'1': 5, '2': 7, '3': 10},
                {'1': 2, '2': 3, '3': 4},
                {'1': 4, '2': 5, '3': 8},
            ],
            'total': {'1': 11, '2': 15, '3': 22}
        }

        response_expected = {
            'url': 'request.url',
            'intervaled_slot_predictions': predictions_mock['interval'],
            'number_intervals': len(input_mock['intervals']),
            'slot_predictions': predictions_mock['total']
        }

        mocker.patch('api.resources.predict.Predict.get_clinic_settings')
        mocker.patch('api.common.controller.TriageController.TriageController.predict',
                     return_value=predictions_mock)

        response = self.test_client.get('/predict', query_string=input_mock)

        assert response.status_code == 200

        response_data = json.loads(response.data)
        assert response_data['intervaled_slot_predictions'] == response_expected['intervaled_slot_predictions']
        assert response_data['number_intervals'] == response_expected['number_intervals']
        assert response_data['slot_predictions'] == response_expected['slot_predictions']


class TestPredictUnit:
    """
    The `TestPredictUnit` class contains unit tests for predict functions.
    """

    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """

        self.predict = Predict()

    def test_get_clinic_settings_database_error(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Test that database errors will be caught.
        """

        mocker.patch('api.common.database_interaction.DataBase.select',
                     side_effect=RuntimeError('Database error'))

        with pytest.raises(RuntimeError):
            self.predict.get_clinic_settings(3)

    def test_get_clinic_settings_empty_data_error(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Test that retrieving no clinic settings causes an error.
        """

        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=[])

        with pytest.raises(RuntimeError):
            self.predict.get_clinic_settings(3)

    def test_get_clinic_settings_success_singleton(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Test that getting a single clinic setting succeeds.
        """

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

        assert self.predict.get_clinic_settings(
            3) == result_expected

    def test_get_clinic_settings_success_multiple(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Test that getting multiple clinic settings succeeds.
        """

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

        assert self.predict.get_clinic_settings(
            3) == result_expected
