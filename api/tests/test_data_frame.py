"""
This module handles testing for the DataFrame.
"""

import pytest
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
        self.intervals_singleton_mock = [{ 'start': '2020-01-01', 'end': '2020-02-01'}]
        self.intervals_multiple_mock = [{ 'start': '2020-01-01', 'end': '2020-02-01'},
                                        { 'start': '2020-02-02', 'end': '2020-03-15'},
                                        { 'start': '2020-03-16', 'end': '2020-04-01'}]

        self.predictions_empty_mock = {1: [], 2: [], 3: []}
        self.predictions_singleton_mock = {1: [(4, 1), (3, 2), (2, 1)]}
        self.predictions_multiple_mock = {
            1: [(4, 1), (3, 2), (2, 1)],
            2: [(3, 4), (2, 1), (1, 2)],
            3: [(4, 1), (2, 4), (6, 2)]
        }

    def test_get_interval_size_invalid_interval_error(self):
        data_frame_empty_intervals = DataFrame(self.intervals_empty_mock, self.predictions_empty_mock)
        dataframe_singleton_intervals = DataFrame(self.intervals_singleton_mock, self.predictions_empty_mock)
        dataframe_multiple_intervals = DataFrame(self.intervals_multiple_mock, self.predictions_empty_mock)

        with pytest.raises(ValueError):
            data_frame_empty_intervals.get_interval_size(1)
        with pytest.raises(ValueError):
            data_frame_empty_intervals.get_interval_size(-1)
        with pytest.raises(ValueError):
            dataframe_singleton_intervals.get_interval_size(1)
        with pytest.raises(ValueError):
            dataframe_singleton_intervals.get_interval_size(-1)
        with pytest.raises(ValueError):
            dataframe_multiple_intervals.get_interval_size(10)
        with pytest.raises(ValueError):
            dataframe_multiple_intervals.get_interval_size(-1)

    def test_get_interval_sample_invalid_interval_error(self):
        data_frame_empty_intervals = DataFrame(self.intervals_empty_mock, self.predictions_empty_mock)
        dataframe_singleton_intervals = DataFrame(self.intervals_singleton_mock, self.predictions_empty_mock)
        dataframe_multiple_intervals = DataFrame(self.intervals_multiple_mock, self.predictions_empty_mock)

        with pytest.raises(ValueError):
            data_frame_empty_intervals.get_interval_sample(1)
        with pytest.raises(ValueError):
            data_frame_empty_intervals.get_interval_sample(-1)
        with pytest.raises(ValueError):
            dataframe_singleton_intervals.get_interval_sample(1)
        with pytest.raises(ValueError):
            dataframe_singleton_intervals.get_interval_sample(-1)
        with pytest.raises(ValueError):
            dataframe_multiple_intervals.get_interval_sample(10)
        with pytest.raises(ValueError):
            dataframe_multiple_intervals.get_interval_sample(-1)

