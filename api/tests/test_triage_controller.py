"""
This module handles testing for the TriageController.
"""

import pytest
from datetime import datetime
from api.common.controller.TriageController import TriageController

class TestTriageController:
    """
    The `TestTriageController` class contains tests for the TriageController.
    """

    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """

        self.intervals_empty_mock = []
        self.intervals_singleton_mock = [('2020-01-01', '2020-02-01')]
        self.intervals_multiple_mock = [('2020-01-01', '2020-02-01'),
                                        ('2020-02-02', '2020-03-15'),
                                        ('2020-03-16', '2020-04-01')]

        self.clinic_settings_mock = [
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
                'duration': 12,
                'proportion': 0.6
            }
        ]

        self.padding_length_small_mock = 7
        self.padding_length_large_mock = 30

    def test_get_historic_data_year_error(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that an error occurs when no historic data is found.
        """

        test_triage_controller = TriageController(self.intervals_multiple_mock,
                                                  self.clinic_settings_mock,
                                                  self.padding_length_large_mock)

        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=[])

        with pytest.raises(RuntimeError):
            test_triage_controller.get_historic_data_year(
                self.intervals_multiple_mock[0][0])

    def test_get_historic_data_year_success(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that a historic data year can be successfully found.
        """

        test_triage_controller = TriageController(self.intervals_multiple_mock,
                                                  self.clinic_settings_mock,
                                                  self.padding_length_large_mock)
        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=[['2019']])

        assert test_triage_controller.get_historic_data_year(
            self.intervals_multiple_mock[0][0]) == 2019

    def test_get_historic_data_referrals(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Tests that historic referal data is properly retrieved.
        """

        test_triage_controller = TriageController(self.intervals_multiple_mock,
                                                  self.clinic_settings_mock,
                                                  self.padding_length_large_mock)

        database_mock = [
            ['2019-01-01', '2019-01-12'],
            ['2019-01-03', '2019-01-14'],
            ['2019-01-05', '2019-01-15'],
            ['2019-01-10', '2019-01-22']
        ]
        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=database_mock)

        expected_response_mock = [
            {'date_recieved': '2019-01-01', 'date_seen': '2019-01-12'},
            {'date_recieved': '2019-01-03', 'date_seen': '2019-01-14'},
            {'date_recieved': '2019-01-05', 'date_seen': '2019-01-15'},
            {'date_recieved': '2019-01-10', 'date_seen': '2019-01-22'}
        ]

        actual_response = test_triage_controller.get_historic_data_referrals(
            self.intervals_multiple_mock[0][0], 2019, 12)

        assert actual_response == expected_response_mock

    def test_sort_referral_data_empty(self):
        """
        Test Type: Unit
        Test Purpose: Tests that empty historic data can be sorted by triage class.
        """

        test_triage_controller = TriageController(self.intervals_multiple_mock,
                                                  self.clinic_settings_mock,
                                                  self.padding_length_large_mock)

        expected_response = {
            1: [],
            2: [],
            3: []
        }

        actual_response = test_triage_controller.sort_referral_data([], self.clinic_settings_mock)

        assert actual_response == expected_response

    def test_sort_referral_data_singleton(self):
        """
        Test Type: Unit
        Test Purpose: Tests that singleton historic data can be sorted by triage class.
        """

        test_triage_controller = TriageController(self.intervals_multiple_mock,
                                                  self.clinic_settings_mock,
                                                  self.padding_length_large_mock)
        referral_data_mock = [
            {
                'date_recieved': datetime.strptime('2019-01-01', '%Y-%m-%d'),
                'date_seen': datetime.strptime('2019-01-02', '%Y-%m-%d')
            }
        ]
        expected_response = {
            1: ['2019-01-01'],
            2: [],
            3: []
        }

        actual_response = test_triage_controller.sort_referral_data(referral_data_mock, self.clinic_settings_mock)

        assert actual_response == expected_response

    def test_sort_referral_data_multiple_same_class(self):
        """
        Test Type: Unit
        Test Purpose: Tests that multiple historic data can be sorted into a single triage class.
        """

        test_triage_controller = TriageController(self.intervals_multiple_mock,
                                                  self.clinic_settings_mock,
                                                  self.padding_length_large_mock)
        referral_data_mock = [
            {
                'date_recieved': datetime.strptime('2019-01-01', '%Y-%m-%d'),
                'date_seen': datetime.strptime('2019-01-01', '%Y-%m-%d')
            },
            {
                'date_recieved': datetime.strptime('2019-01-02', '%Y-%m-%d'),
                'date_seen': datetime.strptime('2019-01-04', '%Y-%m-%d')
            },
            {
                'date_recieved': datetime.strptime('2019-01-03', '%Y-%m-%d'),
                'date_seen': datetime.strptime('2019-01-17', '%Y-%m-%d')
            },
            {
                'date_recieved': datetime.strptime('2019-01-10', '%Y-%m-%d'),
                'date_seen': datetime.strptime('2019-12-31', '%Y-%m-%d')
            }
        ]
        expected_response = {
            1: ['2019-01-01', '2019-01-02', '2019-01-03', '2019-01-10'],
            2: [],
            3: []
        }

        actual_response = test_triage_controller.sort_referral_data(referral_data_mock, self.clinic_settings_mock)

        assert actual_response == expected_response

    def test_sort_referral_data_multiple_all_classes(self):
        """
        Test Type: Unit
        Test Purpose: Tests that multiple historic data can be sorted into multiple triage classes.
        """

        test_triage_controller = TriageController(self.intervals_multiple_mock,
                                                  self.clinic_settings_mock,
                                                  self.padding_length_large_mock)
        referral_data_mock = [
            {
                'date_recieved': datetime.strptime('2019-01-01', '%Y-%m-%d'),
                'date_seen': datetime.strptime('2019-01-01', '%Y-%m-%d')
            },
            {
                'date_recieved': datetime.strptime('2019-01-15', '%Y-%m-%d'),
                'date_seen': datetime.strptime('2019-01-23', '%Y-%m-%d')
            },
            {
                'date_recieved': datetime.strptime('2019-01-02', '%Y-%m-%d'),
                'date_seen': datetime.strptime('2019-01-26', '%Y-%m-%d')
            },
            {
                'date_recieved': datetime.strptime('2019-01-03', '%Y-%m-%d'),
                'date_seen': datetime.strptime('2019-03-17', '%Y-%m-%d')
            }
        ]
        expected_response = {
            1: ['2019-01-01', '2019-01-15'],
            2: ['2019-01-02'],
            3: ['2019-01-03']
        }

        actual_response = test_triage_controller.sort_referral_data(referral_data_mock, self.clinic_settings_mock)

        assert actual_response == expected_response

    def test_get_predictions(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-6 / MOD-7
        """

        assert False

    def test_run_simulation(self):
        """
        Test Type: Acceptance
        Test Purpose: Tests Requirement INT-6 / SIM-1
        """
        
        assert False
