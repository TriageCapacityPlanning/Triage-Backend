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
        self.intervals_singleton_mock = [('2020-01-01', '2020-02-01')]
        self.intervals_multiple_mock = [('2020-01-01', '2020-02-01'),
                                        ('2020-02-02', '2020-03-15'),
                                        ('2020-03-16', '2020-04-01')]

        self.padding_empty_mock = {1: [], 2: [], 3: []}
        self.padding_singleton_mock = {1: [5], 2: [6], 3: [7]}
        self.padding_multiple_mock = {1: [5, 7, 3], 2: [6, 7, 4], 3: [7, 9, 7]}

        self.predictions_empty_mock = {1: [], 2: [], 3: []}
        self.predictions_singleton_mock = {1: [(4, 1), (3, 2), (2, 1)]}
        self.predictions_multiple_mock = {
            1: [(4, 1), (3, 2), (2, 1)],
            2: [(3, 4), (2, 1), (1, 2)],
            3: [(4, 1), (2, 4), (6, 2)]
        }

    def test_get_interval_dates_empty_padding(self):
        """
        Test Type: Unit
        Test Purpose: Tests if intervals are generated properly with no padding.
        """

        empty_interval_data_frame = DataFrame(self.intervals_empty_mock,
                                              self.padding_empty_mock,
                                              self.predictions_multiple_mock)
        single_interval_data_frame = DataFrame(self.intervals_singleton_mock,
                                               self.padding_empty_mock,
                                               self.predictions_multiple_mock)
        multiple_intervals_data_frame = DataFrame(self.intervals_multiple_mock,
                                                  self.padding_empty_mock,
                                                  self.predictions_multiple_mock)

        assert empty_interval_data_frame.get_intervals() == []
        assert single_interval_data_frame.get_intervals() == [(0, 31)]
        assert multiple_intervals_data_frame.get_intervals() == [
            (0, 31), (32, 74), (75, 91)]

    def test_get_interval_dates_singleton_padding(self):
        """
        Test Type: Unit
        Test Purpose: Tests if intervals are generated properly with one padding value.
        """

        empty_interval_data_frame = DataFrame(self.intervals_empty_mock,
                                              self.padding_singleton_mock,
                                              self.predictions_multiple_mock)
        single_interval_data_frame = DataFrame(self.intervals_singleton_mock,
                                               self.padding_singleton_mock,
                                               self.predictions_multiple_mock)
        multiple_intervals_data_frame = DataFrame(self.intervals_multiple_mock,
                                                  self.padding_singleton_mock,
                                                  self.predictions_multiple_mock)

        assert empty_interval_data_frame.get_intervals() == []
        assert single_interval_data_frame.get_intervals() == [(1, 32)]
        assert multiple_intervals_data_frame.get_intervals() == [
            (1, 32), (33, 75), (76, 92)]

    def test_get_interval_dates_multiple_padding(self):
        """
        Test Type: Unit
        Test Purpose: Tests if intervals are generated properly with multiple padding values.
        """

        empty_interval_data_frame = DataFrame(self.intervals_empty_mock,
                                              self.padding_multiple_mock,
                                              self.predictions_multiple_mock)
        single_interval_data_frame = DataFrame(self.intervals_singleton_mock,
                                               self.padding_multiple_mock,
                                               self.predictions_multiple_mock)
        multiple_intervals_data_frame = DataFrame(self.intervals_multiple_mock,
                                                  self.padding_multiple_mock,
                                                  self.predictions_multiple_mock)

        assert empty_interval_data_frame.get_intervals() == []
        assert single_interval_data_frame.get_intervals() == [(3, 34)]
        assert multiple_intervals_data_frame.get_intervals() == [
            (3, 34), (35, 77), (78, 94)]

    def test_get_sample_invalid_triage_class(self):
        """
        Test Type: Unit
        Test Purpose: Tests if generating a sample for an invalid triage class fails.
        """

        test_data_frame = DataFrame(self.intervals_empty_mock,
                                    self.padding_multiple_mock,
                                    self.predictions_multiple_mock)
        with pytest.raises(ValueError):
            test_data_frame.get_sample(-1)

        with pytest.raises(ValueError):
            test_data_frame.get_sample(4)

    def test_get_sample_empty_predictions(self):
        """
        Test Type: Unit
        Test Purpose: Tests getting a sample with no predictions provided.
        """

        empty_padding_data_frame = DataFrame(self.intervals_multiple_mock,
                                             self.padding_empty_mock,
                                             self.predictions_empty_mock)
        single_padding_data_frame = DataFrame(self.intervals_multiple_mock,
                                              self.padding_singleton_mock,
                                              self.predictions_empty_mock)
        multiple_padding_data_frame = DataFrame(self.intervals_multiple_mock,
                                                self.padding_multiple_mock,
                                                self.predictions_empty_mock)

        assert len(empty_padding_data_frame.get_sample(1)) == len(self.padding_empty_mock[1])
        assert len(single_padding_data_frame.get_sample(1)) == len(self.padding_singleton_mock[1])
        assert len(multiple_padding_data_frame.get_sample(1)) == len(self.padding_multiple_mock[1])

    def test_get_sample_singleton_predictions(self):
        """
        Test Type: Unit
        Test Purpose: Tests getting a sample with a single prediction provided.
        """

        empty_padding_data_frame = DataFrame(self.intervals_multiple_mock,
                                             self.padding_empty_mock,
                                             self.predictions_singleton_mock)
        single_padding_data_frame = DataFrame(self.intervals_multiple_mock,
                                              self.padding_singleton_mock,
                                              self.predictions_singleton_mock)
        multiple_padding_data_frame = DataFrame(self.intervals_multiple_mock,
                                                self.padding_multiple_mock,
                                                self.predictions_singleton_mock)

        assert len(empty_padding_data_frame.get_sample(1)) == \
               len(self.padding_empty_mock[1]) + len(self.predictions_singleton_mock[1])

        assert len(single_padding_data_frame.get_sample(1)) == \
               len(self.padding_singleton_mock[1]) + len(self.predictions_singleton_mock[1])

        assert len(multiple_padding_data_frame.get_sample(1)) == \
               len(self.padding_multiple_mock[1]) + len(self.predictions_singleton_mock[1])

    def test_get_sample_multiple_predictions(self):
        """
        Test Type: Unit
        Test Purpose: Tests getting a sample with multiple predictions provided.
        """
        
        empty_padding_data_frame = DataFrame(self.intervals_multiple_mock,
                                             self.padding_empty_mock,
                                             self.predictions_multiple_mock)
        single_padding_data_frame = DataFrame(self.intervals_multiple_mock,
                                              self.padding_singleton_mock,
                                              self.predictions_multiple_mock)
        multiple_padding_data_frame = DataFrame(self.intervals_multiple_mock,
                                                self.padding_multiple_mock,
                                                self.predictions_multiple_mock)

        assert len(empty_padding_data_frame.get_sample(1)) == \
               len(self.padding_empty_mock[1]) + len(self.predictions_multiple_mock[1])

        assert len(single_padding_data_frame.get_sample(1)) == \
               len(self.padding_singleton_mock[1]) + len(self.predictions_multiple_mock[1])

        assert len(multiple_padding_data_frame.get_sample(1)) == \
               len(self.padding_multiple_mock[1]) + len(self.predictions_multiple_mock[1])

    def test_generate_sample_value(self):
        """
        Test Type: Unit
        Test Purpose: Tests if a generated sample value is within the proper range.
        """
        
        test_data_frame = DataFrame(self.intervals_multiple_mock,
                                    self.padding_multiple_mock,
                                    self.predictions_multiple_mock)

        prediction_mock = (5, 2)

        result = test_data_frame.generate_sample_value(prediction_mock)

        assert result >= prediction_mock[0] - prediction_mock[1]
        assert result <= prediction_mock[0] + prediction_mock[1]
