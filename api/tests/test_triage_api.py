"""
This module handles acceptance testing for the TriageAPI.
"""

from api.triage_api import create_app
import json


class TestTriageAPI:
    """
    The `TestTriageAPI` class contains acceptance tests for general API functions.
    """

    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """
        
        self.test_client = create_app().test_client()

    def test_base_route(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-4
        """

        response = self.test_client.get('/')
        response_data = json.loads(response.data)

        assert response.status_code == 200
        assert response_data['api'] == 'Triage API'

    def test_base_route_version(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-5
        """

        response = self.test_client.get('/v1')
        response_data = json.loads(response.data)

        assert response.status_code == 200
        assert response_data['version'] == 1
