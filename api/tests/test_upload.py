"""
This module handles testing for the Upload class.
"""

import pytest
import json
from api.resources.upload import Waitlist, PastAppointments
from api.triage_api import create_app


class TestUploadWaitlistAPI:
    """
    The `TestUploadAPI` class contains acceptance tests for upload API functions.
    """

    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """

        self.test_client = create_app().test_client()

    def test_put_missing_inputs(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-7, DAT-1, DAT-4
        """

        input_mock = {}
        response = self.test_client.put('/upload/waitlist', json=input_mock)

        assert response.status_code == 422

    def test_put_incorrect_input_type_clinic_id(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-7, DAT-1, DAT-4
        """

        input_mock = {
            'clinic-id': '"1"',
            'upload-data': ""
        }
        response = self.test_client.put('/upload/waitlist', json=input_mock)

        assert response.status_code == 422

    def test_upload_success(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-7, DAT-1, DAT-4
        """
        input_mock = {
            'clinic-id': 1,
            'upload-data': "data.csv"
        }

        response = self.test_client.put('/upload/waitlist', json=input_mock)

        assert response.status_code == 200


class TestUploadPastAppointmentsAPI:
    """
    The `TestUploadAPI` class contains acceptance tests for upload API functions.
    """

    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """

        self.test_client = create_app().test_client()

    def test_put_missing_inputs(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-7, DAT-1, DAT-4
        """

        input_mock = {}
        response = self.test_client.put('/upload/past-appointments', json=input_mock)

        assert response.status_code == 422

    def test_put_incorrect_input_type_clinic_id(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-7, DAT-1, DAT-4
        """

        input_mock = {
            'clinic-id': '"1"',
            'upload-data': ""
        }
        response = self.test_client.put('/upload/past-appointments', json=input_mock)

        assert response.status_code == 422

    def test_upload_success(self, mocker):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-7, DAT-1, DAT-4
        """
        input_mock = {
            'clinic-id': 1,
            'upload-data': "data.csv"
        }

        response = self.test_client.put('/upload/past-appointments', json=input_mock)

        assert response.status_code == 200


class TestWaitlistUnit:
    """
    The `TestWaitlistUnit` class contains unit tests for predict functions.
    """

    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """
        self.waitlist = Waitlist()


class TestPastAppointmentsUnit:
    """
    The `TestPastAppointmentsUnit` class contains unit tests for predict functions.
    """

    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """
        self.pastappointments = PastAppointments()
