"""
This module handles testing for the UpdateTriageClasses class.
"""

from api.resources.update_triage_classes import UpdateTriageClasses
from api.triage_api import create_app
import pytest
import json


class TestUpdateTriageClassesAPI:
    """
    The `TestUpdateTriageClassesAPI` class contains acceptance tests the UpdateTriageClasses class.
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
        response = self.test_client.get('/classes', query_string=input_mock)

        assert response.status_code == 422

    def test_get_incorrect_input_type(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-6
        """

        input_mock = {'clinic-id': '"1"'}
        response = self.test_client.get('/classes', query_string=input_mock)

        assert response.status_code == 422

    def test_get_triage_classes_success_singleton(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-6
        """

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
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-6
        """

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
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement DAT-4
        """

        input_mock = {}
        response = self.test_client.put('/classes', json=(input_mock))

        assert response.status_code == 422

    def test_put_incorrect_input_type(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement DAT-4
        """

        input_mock = {'triage-class': '"1"'}
        response = self.test_client.put('/classes', json=(input_mock))

        assert response.status_code == 422

    def test_put_triage_classes_success_singleton(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement DAT-4
        """

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
    """
    The `TestUpdateTriageClassesUnit` class contains unit tests for the UpdateTriageClasses class.
    """

    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """

        self.update_triage_classes = UpdateTriageClasses()

    def test_get_triage_classes_database_error(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Test that database errors are caught when retrieving clinic settings.
        """

        mocker.patch('api.common.database_interaction.DataBase.select',
                     side_effect=RuntimeError('Database error'))

        with pytest.raises(RuntimeError):
            self.update_triage_classes.get_triage_classes(3)

    def test_get_triage_classes_empty_data_error(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Test that retrieving no clinic settings results in an error.
        """

        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=[])

        with pytest.raises(RuntimeError):
            self.update_triage_classes.get_triage_classes(3)

    def test_get_triage_classes_success_singleton(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Test that singleton clinic settings are properly retrieved.
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

        assert self.update_triage_classes.get_triage_classes(
            3) == result_expected

    def test_get_triage_classes_success_multiple(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Test that multiple clinic settings are properly retrieved.
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

        assert self.update_triage_classes.get_triage_classes(
            3) == result_expected

    def test_update_triage_class_database_error(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Test that database errors are caught when updating clinic settings.
        """

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
        """
        Test Type: Unit
        Test Purpose: Test that clinic settings are properly updated.
        """

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
        except:
            raise pytest.fail('Did raise exception')
