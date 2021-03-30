"""
This module handles testing for the DataFrame.
"""

import pytest
from datetime import datetime
from api.common.controller.DataFrame import DataFrame

class TestDataFrame:
    """
    The `TestDataFRame` class contains acceptance and unit tests for the DataFrame.
    """

    def setup_class(self):
        """
        Test setup that occurs once before all tests are run.
        """

        self.intervals_empty_mock = []
        self.intervals_singleton_mock = [{ 'start': datetime.strptime('2020-01-01','%Y-%m-%d'), 'end': datetime.strptime('2020-02-01','%Y-%m-%d')}]
        self.intervals_multiple_mock = [{ 'start': datetime.strptime('2020-01-01','%Y-%m-%d'), 'end': datetime.strptime('2020-02-01','%Y-%m-%d')},
                                        { 'start': datetime.strptime('2020-02-02','%Y-%m-%d'), 'end': datetime.strptime('2020-03-15','%Y-%m-%d')},
                                        { 'start': datetime.strptime('2020-03-16','%Y-%m-%d'), 'end': datetime.strptime('2020-04-01','%Y-%m-%d')}]

        self.predictions_empty_mock = []
        self.predictions_mock = [(4, 1), (3, 2), (2, 1), (4, 2), (2, 2)]

        self.padding_length_empty_mock = 0
        self.padding_length_singleton_mock = 1

    def test_get_interval_size_invalid_interval_error(self):
        data_frame_empty_intervals = DataFrame(self.predictions_empty_mock, 
                                               self.intervals_empty_mock, 
                                               self.padding_length_empty_mock)
        dataframe_singleton_intervals = DataFrame(self.predictions_mock, 
                                                  self.intervals_singleton_mock,
                                                  self.padding_length_empty_mock)
        dataframe_multiple_intervals = DataFrame(self.predictions_mock, 
                                                 self.intervals_multiple_mock,
                                                 self.padding_length_empty_mock)

        with pytest.raises(ValueError):
            data_frame_empty_intervals.get_interval_size(10)
        with pytest.raises(ValueError):
            data_frame_empty_intervals.get_interval_size(-1)
        with pytest.raises(ValueError):
            dataframe_singleton_intervals.get_interval_size(10)
        with pytest.raises(ValueError):
            dataframe_singleton_intervals.get_interval_size(-1)
        with pytest.raises(ValueError):
            dataframe_multiple_intervals.get_interval_size(10)
        with pytest.raises(ValueError):
            dataframe_multiple_intervals.get_interval_size(-1)

    def test_get_interval_size_success_one_week_interval(self):
        interval_zero_mock = [{ 'start': datetime.strptime('2020-01-01','%Y-%m-%d'), 'end': datetime.strptime('2020-01-01','%Y-%m-%d')}]
        data_frame_zero_interval = DataFrame(self.predictions_empty_mock, 
                                               interval_zero_mock, 
                                               self.padding_length_empty_mock)
        
        assert data_frame_zero_interval.get_interval_size(0) == 1
    
    def test_get_interval_size_success_multiple_weeks_interval(self):
        data_frame_multiple_interval = DataFrame(self.predictions_empty_mock, 
                                             self.intervals_singleton_mock, 
                                             self.padding_length_empty_mock)
        
        assert data_frame_multiple_interval.get_interval_size(0) == 5

    def test_get_interval_sample_invalid_interval_error(self):
        data_frame_empty_intervals = DataFrame(self.predictions_empty_mock, 
                                               self.intervals_empty_mock, 
                                               self.padding_length_empty_mock)
        dataframe_singleton_intervals = DataFrame(self.predictions_empty_mock, 
                                                  self.intervals_singleton_mock,
                                                  self.padding_length_empty_mock)
        dataframe_multiple_intervals = DataFrame(self.predictions_empty_mock, 
                                                 self.intervals_multiple_mock,
                                                 self.padding_length_empty_mock)

        with pytest.raises(ValueError):
            data_frame_empty_intervals.get_interval_sample(10)
        with pytest.raises(ValueError):
            data_frame_empty_intervals.get_interval_sample(-1)
        with pytest.raises(ValueError):
            dataframe_singleton_intervals.get_interval_sample(10)
        with pytest.raises(ValueError):
            dataframe_singleton_intervals.get_interval_sample(-1)
        with pytest.raises(ValueError):
            dataframe_multiple_intervals.get_interval_sample(10)
        with pytest.raises(ValueError):
            dataframe_multiple_intervals.get_interval_sample(-1)

    def test_get_interval_sample_success(self):
        dataframe = DataFrame(self.predictions_mock, 
                                                 self.intervals_singleton_mock,
                                                 self.padding_length_empty_mock)

        interval_sample = dataframe.get_interval_sample(0)

        assert len(interval_sample) == dataframe.get_interval_size(0)

        for sample in zip(interval_sample, self.predictions_mock):
            assert sample[0] >= 0