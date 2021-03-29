"""
This module handles testing for the DataFrame.
"""

import pytest
from api.common.ClinicData import ClinicData


class TestClinicData:
    """
    The `TestDataFRame` class contains acceptance and unit tests for the DataFrame.
    """

    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """
        self.clinic_id_mock = 1
        self.triage_class_mock = 1
        self.interval_mock = ['2020-01-01', '2021-01-01']

    def test_no_clinic_settings_error(self, mocker):
        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=[])
        
        with pytest.raises(RuntimeError):
            ClinicData(self.clinic_id_mock)

    def test_get_clinic_settings_success_singleton(self, mocker):
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

        clinic_data = ClinicData(self.clinic_id_mock)
        assert clinic_data.get_clinic_settings() == result_expected

    def test_get_clinic_settings_success_multiple(self, mocker):
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

        clinic_data = ClinicData(1)
        assert clinic_data.get_clinic_settings() == result_expected

    def test_get_referral_data_success_empty(self, mocker):
        database_clinic_settings_response_mock = [[3, 1, 'Urgent', 2, 0.8]]
        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=database_clinic_settings_response_mock)
        
        clinic_data = ClinicData(self.clinic_id_mock)

        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=[])

        assert clinic_data.get_referral_data(self.triage_class_mock, self.interval_mock) == []

    def test_get_referral_data_success_singleton(self, mocker):
        database_clinic_settings_response_mock = [[3, 1, 'Urgent', 2, 0.8]]
        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=database_clinic_settings_response_mock)
        
        clinic_data = ClinicData(self.clinic_id_mock)

        database_referral_data_mock = [
            ('2020-01-01', '2020-01-14')
        ]
        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=database_referral_data_mock)

        expected_result = [(self.clinic_id_mock, self.triage_class_mock, '2020-01-01', '2020-01-14')]
        assert clinic_data.get_referral_data(self.triage_class_mock, self.interval_mock) == expected_result

    def test_get_referral_data_success_multiple(self, mocker):
        database_clinic_settings_response_mock = [[3, 1, 'Urgent', 2, 0.8]]
        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=database_clinic_settings_response_mock)
        
        clinic_data = ClinicData(self.clinic_id_mock)

        database_referral_data_mock = [
            ('2020-01-01', '2020-01-14'),
            ('2020-05-01', '2020-05-14'),
            ('2020-11-01', '2020-11-14'),
        ]
        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=database_referral_data_mock)

        expected_result = [
            (self.clinic_id_mock, self.triage_class_mock, '2020-01-01', '2020-01-14'),
            (self.clinic_id_mock, self.triage_class_mock, '2020-05-01', '2020-05-14'),
            (self.clinic_id_mock, self.triage_class_mock, '2020-11-01', '2020-11-14')
        ]
        assert clinic_data.get_referral_data(self.triage_class_mock, self.interval_mock) == expected_result

    def test_update_triage_class_database_error(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Test that database errors are caught when updating clinic settings.
        """

        database_clinic_settings_response_mock = [[3, 1, 'Urgent', 2, 0.8]]
        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=database_clinic_settings_response_mock)
        
        clinic_data = ClinicData(self.clinic_id_mock)

        triage_class_input = {
            'clinic_id': 3,
            'severity': 1,
            'name': 'Urgent',
            'duration': 2,
            'proportion': 0.8
        }

        mocker.patch('api.common.database_interaction.DataBase.insert',
                    side_effect=RuntimeError('Database error'))

        with pytest.raises(RuntimeError):
            clinic_data.update_triage_class(triage_class_input)

    def test_update_triage_class_database_success(self, mocker):
        """
        Test Type: Unit
        Test Purpose: Test that clinic settings are properly updated.
        """

        database_clinic_settings_response_mock = [[3, 1, 'Urgent', 2, 0.8]]
        mocker.patch('api.common.database_interaction.DataBase.select',
                     return_value=database_clinic_settings_response_mock)
        
        clinic_data = ClinicData(self.clinic_id_mock)

        triage_class_input = {
            'clinic_id': 3,
            'severity': 1,
            'name': 'Urgent',
            'duration': 2,
            'proportion': 0.8
        }

        mocker.patch('api.common.database_interaction.DataBase.insert')

        try:
            clinic_data.update_triage_class(triage_class_input)
        except:
            raise pytest.fail('Did raise exception')
