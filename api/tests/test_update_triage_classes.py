"""
This module handles testing for the UpdateTriageClasses class.
"""

from api.resources.update_triage_classes import UpdateTriageClasses
from api.triage_api import create_app
from api.common.config import VERSION_PREFIX
import pytest
import json

from api.tests.common import generate_token

class TestUpdateTriageClassesAPI:
    """
    The `TestUpdateTriageClassesAPI` class contains acceptance tests the UpdateTriageClasses class.
    """

    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """
        self.token = generate_token('username', 1)
        self.endpoint = VERSION_PREFIX + '/classes'
        self.test_client = create_app().test_client()

    def test_get_missing_inputs(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-6
        """

        input_mock = {}
        response = self.test_client.get(self.endpoint, headers={'token': self.token}, query_string=input_mock)

        assert response.status_code == 422

    def test_get_incorrect_input_type(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-6
        """

        input_mock = {'clinic_id': "'1'" }
        response = self.test_client.get(self.endpoint, headers={'token': self.token}, query_string=input_mock)

        assert response.status_code == 500

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
        mocker.patch('api.common.ClinicData.ClinicData.__init__', return_value=None)
        mocker.patch('api.common.ClinicData.ClinicData.get_clinic_settings',
                     return_value=triage_classes_mock)

        input_mock = {'clinic_id': 1}
        response = self.test_client.get(self.endpoint, headers={'token': self.token}, query_string=input_mock)

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
        mocker.patch('api.common.ClinicData.ClinicData.__init__', return_value=None)
        mocker.patch('api.common.ClinicData.ClinicData.get_clinic_settings',
                     return_value=triage_classes_mock)

        input_mock = {'clinic_id': 1}
        response = self.test_client.get(self.endpoint, headers={'token': self.token}, query_string=input_mock)

        assert response.status_code == 200
        assert json.loads(response.data)['classes'] == triage_classes_mock

    def test_put_missing_inputs(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement DAT-4
        """

        input_mock = {}
        response = self.test_client.put(self.endpoint, headers={'token': self.token}, json=(input_mock))

        assert response.status_code == 422

    def test_put_incorrect_input_type(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement DAT-4
        """

        input_mock = {'triage_class': '"1"'}
        response = self.test_client.put(self.endpoint, headers={'token': self.token}, json=(input_mock))

        assert response.status_code == 422

    def test_put_triage_classes_success_singleton(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement DAT-4
        """
        mocker.patch('api.common.ClinicData.ClinicData.__init__', return_value=None)
        mocker.patch('api.common.ClinicData.ClinicData.update_triage_class')

        triage_class_mock = {
            'clinic_id': 1,
            'severity': 1,
            'name': 'Urgent',
            'duration': 2,
            'proportion': 0.8
        }
        input_mock = {
            'triage_class': triage_class_mock
        }
        response = self.test_client.put(self.endpoint, headers={'token': self.token}, json=(input_mock))
        assert response.status_code == 200
        assert json.loads(response.data)['updated'] == triage_class_mock