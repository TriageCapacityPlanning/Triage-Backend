"""
The DataFrame is used to generate varying sets of referal predictions for the purposes of simulation.
"""

# External dependencies
import random
from datetime import datetime

class DataFrame:
    """
    DataFrame is a class to generate data for simulating patient referals.

    Usage:
        To create a new data frame, create it with `DataFrame(intervals, predictions, distribution)`.

    Args:
        intervals (list): List of interval start and end dates.
        paddings (tuple): 2-ary tuple containing start and end padding.
        predictions (list): List of predictions for each interval.
        distribution (dict): Distribution of patients by triage class.
    """

    def __init__(self, intervals, predictions, padding_lengths):
        self.intervals = self.__format_dates_to_indexes(
            intervals, padding_lengths)
        self.predictions = predictions

    def get_interval_size(self, interval):
        '''Returns the size of a given interval.

        Parameters:
            `interval` (int): The index of an interval
        Returns:
            Returns the size of the given interval

        '''

        # Check validity of input interval index.
        if interval not in range(0, len(self.intervals)):
            raise ValueError("Invalid interval %s.", interval)

        # Return the length of a given interval
        return self.intervals[interval][1] - self.intervals[interval][0] + 1
    
    def get_interval_sample(self, interval):
        '''Returns a sample for a given interval

        Parameters:
            `interval` (int): The index of an interval
        Returns:
            Returns a sample list of patient arrivals for the interval.

        '''

        # Check validity of input interval index.
        if interval not in range(0, len(self.intervals)):
            raise ValueError("Invalid interval %s.", interval)
        
        # Get start and end of interval
        start = self.intervals[interval][0]
        end = self.intervals[interval][1]+1

        # Generate and return sample
        return [self.generate_sample_value(p) for p in self.predictions[start:end]]

    def generate_sample_value(self, prediction):
        """Generates a random arrival count value given a prediction containing a base arrival count and variance value.

        Parameters:
            `prediction` (tuple): A tuple with the base prediction value followed by the variance.

        Returns:
            Returns an integer prediction of the number of referals.
        """

        variance = random.uniform(-prediction[1], prediction[1])
        return int(prediction[0] + variance)

    def __format_dates_to_indexes(self, intervals, padding_lengths):
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
        date_offsets = [(datetime.strptime(interval[1], '%Y-%m-%d') - datetime.strptime(interval[0], '%Y-%m-%d')).days
                        for interval in intervals]

        interval_start_index = padding_lengths[0]
        interval_indexes = [(0, padding_lengths[0]-1)]
        for offset in date_offsets:
            interval_indexes.append((interval_start_index, interval_start_index + offset))
            interval_start_index += offset + 1

        return interval_indexes + [(interval_start_index, interval_start_index + padding_lengths[1])]
