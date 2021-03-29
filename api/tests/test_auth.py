"""
This module handles testing for the UpdateTriageClasses class.
"""

from api.triage_api import create_app
from api.common.config import VERSION_PREFIX
import pytest
import json
import os
import jwt
import hashlib

from api.tests.common import generate_token

class TestAuthAPI:
    """
    The `TestAuth` class contains acceptance tests the UpdateTriageClasses class.
    """

    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """
        self.endpoint = VERSION_PREFIX + '/auth/login'
        self.test_client = create_app().test_client()

    def test_post_missing_inputs(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-6
        """

        input_mock = {}
        response = self.test_client.post(self.endpoint, json=input_mock)

        assert response.status_code == 422

    def test_post_incorrect_input_type(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-6
        """

        input_mock = {'username': 1, 'password': 2 }
        response = self.test_client.post(self.endpoint, json=input_mock)

        assert response.status_code == 422

    def test_post_success(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-6
        """
        mocker.patch('api.common.database_interaction.DataBase.select', 
                     return_value=[(1, True, hashlib.sha512('passwordsalt'.encode()).hexdigest(), 'salt')])

        input_mock = {'username': 'username', 'password': 'password' }
        response = self.test_client.post(self.endpoint, json=input_mock)

        assert response.status_code == 200

        response_data = json.loads(json.loads(response.data.decode("utf-8")))

        expected_token_data = {
            'user': 'username',
            'clinic': 1,
            'admin': True
        }
        
        assert 'token' in response_data
        assert response_data['clinic_id'] == expected_token_data['clinic']
        assert response_data['admin'] == expected_token_data['admin']
        
        data = jwt.decode(response_data['token'], os.environ['API_SECRET'], algorithms=["HS256"])
        assert data['user'] == expected_token_data['user']
        assert data['clinic'] == expected_token_data['clinic']