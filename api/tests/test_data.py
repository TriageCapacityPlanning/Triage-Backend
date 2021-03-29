"""
This module handles testing for the UpdateTriageClasses class.
"""

from api.triage_api import create_app
from api.common.config import VERSION_PREFIX
import pytest
import json

from api.tests.common import generate_token

class TestDataAPI:
    """
    The `TestAuth` class contains acceptance tests the UpdateTriageClasses class.
    """

    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """
        self.token = generate_token('username', 1)
        self.endpoint = VERSION_PREFIX + '/data/1/1'
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

        input_mock = {'interval': "1"}

        result = self.test_client.get(self.endpoint, headers={'token': self.token}, query_string=input_mock)
        assert result.status_code == 500

    def test_get_success_empty(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-6
        """
        mocker.patch('api.common.ClinicData.ClinicData.__init__', return_value=None)
        
        return_data_mock = []
        mocker.patch('api.common.ClinicData.ClinicData.get_referral_data', return_value=return_data_mock)

        input_mock = {'interval': json.dumps(['2020-01-01', '2021-01-01'])}
        response = self.test_client.get(self.endpoint, headers={'token': self.token}, query_string=input_mock)
        
        assert response.status_code == 200
        assert json.loads(response.data) == []
    
    def test_get_success_singleton(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-6
        """
        mocker.patch('api.common.ClinicData.ClinicData.__init__', return_value=None)
        
        return_data_mock = [[1, 1, '2020-01-01', '2020-01-14']]
        mocker.patch('api.common.ClinicData.ClinicData.get_referral_data', return_value=return_data_mock)

        input_mock = {'interval': json.dumps(['2020-01-01', '2021-01-01'])}
        response = self.test_client.get(self.endpoint, headers={'token': self.token}, query_string=input_mock)
        
        assert response.status_code == 200
        assert json.loads(response.data) == return_data_mock

    def test_get_success_singleton(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-6
        """
        mocker.patch('api.common.ClinicData.ClinicData.__init__', return_value=None)
        
        return_data_mock = [
            [1, 1, '2020-01-01', '2020-01-14'],
            [1, 1, '2020-05-01', '2020-05-14'],
            [1, 1, '2020-11-01', '2020-11-14']
        ]
        mocker.patch('api.common.ClinicData.ClinicData.get_referral_data', return_value=return_data_mock)

        input_mock = {'interval': json.dumps(['2020-01-01', '2021-01-01'])}
        response = self.test_client.get(self.endpoint, headers={'token': self.token}, query_string=input_mock)
        
        assert response.status_code == 200
        assert json.loads(response.data) == return_data_mock