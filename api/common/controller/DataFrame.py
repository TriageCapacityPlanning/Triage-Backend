"""
The DataFrame is used to generate varying sets of referal predictions for the purposes of simulation.
"""

# External dependencies
import random
import numpy as np
import math
from datetime import datetime

## TODO : UPDATE INTERVALS TO BE DATES

class DataFrame:
    def __init__(self, predictions, intervals, padding_length):
        self.intervals = self.__format_intervals(intervals, padding_length)
        self.predictions = predictions

    def get_interval_size(self, interval):
        # Check validity of input interval index.
        if interval not in range(0, len(self.intervals)):
            raise ValueError("Invalid interval %s.", interval)

        # Return the length of a given interval
        return (self.intervals[interval][1] - self.intervals[interval][0]) + 1
    
    def get_interval_sample(self, interval):
        # RETURN LIST OF PREDICTIONS LENGTH EQUAL TO WEEKS IN INTERVAL

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
        """
        Converts intervals from date format (start and end date for an interval) to relative
        indexes in the list of predictions.

        Parameters:
            `intervals` (list): List of date string tuples with the start and end dates of the interval.
            `paddings` (tuple): 2-ary tuple containing start and end padding.

        Returns:
            Returns the intervals as a list of tuples with start and end indexes relative to the
            predictions given to the DataFrame.
        """

        formatted_intervals = [(0, padding_length-1)]
        for interval in intervals:
            start = int((interval['start'] - intervals[0]['start']).days / 7) + 30
            end = int((interval['end'] - intervals[0]['start']).days / 7) + 30
            formatted_intervals.append([start, end])

        return formatted_intervals