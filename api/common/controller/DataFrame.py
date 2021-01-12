import random

class DataFrame:
    def __init__(self, intervals, predictions, distribution):
        self.intervals = intervals
        self.predictions = predictions
        self.distribution = distribution

    def get_interval_dates(self, interval: int):
        # Return the dates of a given interval
        return self.intervals[interval]

    def get_sample(self, interval: int, triage_class: int):
        # Find the base prediction of referals relative to a triage class
        base_referal_prediction = self.predictions[interval][0] * self.distribution[triage_class]
        # Generate a variance of referals relative to a triage class
        variance = random.uniform(-self.predictions[interval][1], self.predictions[interval][1]) * self.distribution[triage_class]
        # Sum the base prediction and the variance
        sample = base_referal_prediction + variance
        # Return a valid sample or 0
        return sample if sample > 0 else 0

    def get_distribution(self, interval: int, triage_class: int):
        # Return distribution information for a given interval and triage class pair
        return {
            'start-date': self.intervals[interval][0],
            'end-date': self.intervals[interval][1],
            'predicted-patients': self.predictions[interval][0] * self.distribution[triage_class],
            'predicted-variance': self.predictions[interval][1] * self.distribution[triage_class]
        }