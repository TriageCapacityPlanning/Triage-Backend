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
        predictions (list): List of predictions for each interval.
        distribution (dict): Distribution of patients by triage class.
    """

    def __init__(self, intervals, paddings, predictions):
        self.intervals = self.__format_dates_to_indexes(
            intervals, paddings)
        self.predictions = predictions
        self.paddings = paddings

    def get_intervals(self):
        '''Returns the intervals.

        Returns:
            A list containing an entry for each interval defining the start and end index of predictions in the list.
            Ex. (0, 2)

        '''

        # Return the dates of a given interval
        return self.intervals

    def get_sample(self, triage_class: int):
        """Returns a sample prediction for referal count of patients within a triage class.

        Parameters:
            `triage_class` (int): The severity of the desired triage class.

        Returns:
            Returns a list of integer predictions for the number of referals.
        """

        if triage_class not in self.predictions.keys() or triage_class not in self.paddings.keys():
            raise ValueError("Invalid triage class %s.", triage_class)

        sample = [self.generate_sample_value(p) for p in self.predictions[triage_class]]

        return self.paddings[triage_class] + sample

    def generate_sample_value(self, prediction):
        """Generates a random arrival count value given a prediction containing a base arrival count and variance value.

        Parameters:
            `prediction` (tuple): A tuple with the base prediction value followed by the variance.

        Returns:
            Returns an integer prediction of the number of referals.
        """

        variance = random.uniform(-prediction[1], prediction[1])
        return int(prediction[0] + variance)

    def __format_dates_to_indexes(self, intervals, paddings):
        """Converts intervals from date format (start and end date for an interval) to relative indexes in the list of predictions.

        Parameters:
            `intervals` (list): List of date string tuples with the start and end dates of the interval.
            `paddings` (list): List of padding predictions.

        Returns:
            Returns the intervals as a list of tuples with start and end indexes relative to the predictions given to the DataFrame.
        """

        padding_length = [len(p) for p in paddings.values()][0] if len(paddings) > 0 else 0

        date_offsets = [(datetime.strptime(end, '%Y-%m-%d') - datetime.strptime(start, '%Y-%m-%d')).days
                        for (start, end) in intervals]
        
        interval_start_index = padding_length
        interval_indexes = []
        for offset in date_offsets:
            interval_indexes.append((interval_start_index, interval_start_index + offset))
            interval_start_index += offset + 1
        
        return interval_indexes
