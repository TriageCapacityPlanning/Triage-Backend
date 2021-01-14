""" 
The DataFrame is used to generate varying sets of referal predictions for the purposes of simulation.
"""

# External dependencies
import random


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

    def __init__(self, intervals, predictions, distribution):
        self.intervals = intervals
        self.predictions = predictions
        self.distribution = distribution

    def get_interval_dates(self, interval: int):
        '''Returns the start and end date for a given interval.

        Parameters:
            `interval` (int): The index of the desired interval.

        Returns:
            The start and end date for the given interval as a 2-ary tuple.
            Example: ('2020-01-01', '2020-02-15')

        '''
        # Return the dates of a given interval
        return self.intervals[interval]

    def get_sample(self, interval: int, triage_class: int):
        """Returns a sample prediction for referal count of patients within a triage class for a given interval.

        Parameters:
            `interval` (int): The index of the desired interval.
            `triage_class` (int): The severity of the desired triage class.

        Returns:
            Returns an integer prediction of the number of referals.
        """
        # Find the base prediction of referals relative to a triage class
        base_referal_prediction = self.predictions[interval][0] * self.distribution[triage_class]
        # Generate a variance of referals relative to a triage class
        variance = random.uniform(-self.predictions[interval][1], self.predictions[interval][1]) * self.distribution[triage_class]
        # Sum the base prediction and the variance
        sample = base_referal_prediction + variance
        # Return a valid sample or 0
        return sample if sample > 0 else 0

    def get_distribution(self, interval: int, triage_class: int):
        """Returns distribution information about a given triage class within a provided interval.

        Parameters:
            `interval` (int): The index of the desired interval.
            `triage_class` (int): The severity of the desired triage class.

        Returns:
            A dictionary containing:
                `start-date` (str): Start date of the interval.
                `end-date` (str): End date of the interval.
                `predicted-patients` (int): The predicted referals of the given triage class for the interval.
                `predicted-variance` (int): The predicted variance of referals of the given triage class for the interval.

        """
        # Return distribution information for a given interval and triage class pair
        return {
            'start-date': self.intervals[interval][0],
            'end-date': self.intervals[interval][1],
            'predicted-patients': self.predictions[interval][0] * self.distribution[triage_class],
            'predicted-variance': self.predictions[interval][1] * self.distribution[triage_class]
        }
