"""
The DataFrame is used to generate varying sets of referal predictions for the purposes of simulation.
"""

# External dependencies
import numpy as np
import math


class DataFrame:
    """
    DataFrame is a class to generate data for simulating patient referals.
    Usage:
        To create a new data frame, create it with `DataFrame(intervals, predictions, padding_length)`.

    Args:
        intervals (list): List of interval start and end dates.
        predictions (list): List of predictions and padding data.
        padding_length (dict): Distribution of patients by triage class.
    """

    def __init__(self, predictions, intervals, padding_length):
        self.intervals = self.__format_intervals(intervals, padding_length)
        print(self.intervals)
        self.predictions = predictions

    def get_interval_size(self, interval):
        """Returns the size of an interval (in weeks).
        Parameters:
            `interval` (int): The index of the desired interval.
        Returns:
            Returns an integer value equal to the size of the interval (in weeks).
        """

        # Check validity of input interval index.
        if interval not in range(0, len(self.intervals)):
            raise ValueError("Invalid interval %s.", interval)

        # Return the length of a given interval
        return (self.intervals[interval][1] - self.intervals[interval][0]) + 1

    def get_interval_sample(self, interval):
        """Returns a sample prediction for referal count of patients.
        Parameters:
            `interval` (int): The index of the desired interval.
        Returns:
            Returns a list (of length equal to the number of weeks in the given interval) where each
            entry is an integer signifying the number of patient referrals predicted to arrive.
        """
        # Check validity of input interval index.
        if interval not in range(0, len(self.intervals)):
            raise ValueError("Invalid interval %s.", interval)

        # Get start and end of interval
        start = self.intervals[interval][0]
        end = self.intervals[interval][1] + 1

        # Generate and return sample
        res = [np.round(max(0, np.random.normal(p[0], math.sqrt(p[1])))) for p in self.predictions[start:end]]
        return res

    def __format_intervals(self, intervals, padding_length):
        """Converts intervals from date format (start and end date for an interval) to relative
        indexes in the list of predictions.
        Parameters:
            `intervals` (list): List of date tuples with the start and end dates of the interval.
            `padding_length` (int): The size of the padding data (in weeks).
        Returns:
            Returns the intervals as a list of tuples with start and end indexes relative to the
            predictions given to the DataFrame.
        """

        formatted_intervals = []
        if padding_length != 0:
            formatted_intervals.append((0, padding_length-1))

        for interval in intervals:
            start = int((interval['start'] - intervals[0]['start']).days / 7) + padding_length
            end = int((interval['end'] - intervals[0]['start']).days / 7) + padding_length
            formatted_intervals.append([start, end])

        return formatted_intervals
