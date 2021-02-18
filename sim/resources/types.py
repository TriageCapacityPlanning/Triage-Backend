from collections import deque
from typing import List


class TimeUnitBreakdown:
    """
    Properties
    ----------
    current_time: int
        The date of this time unit
    record: record
        A report on what was processed on this time unit and how many
    total: int
        The total number of arrivals processed on this time unit
    """
    def __init__(self, current_time: int):
        self.current_time = current_time
        self.record = {}
        self.total = 0

    def add(self, creation_time: int, slots: int) -> None:
        """
        Add an arrival's processing record for this time unit. Also updates the total count

        :param creation_time: the creation time id of the arrival (as a time unit)
        :param slots: the number of slots for the arrival that were processed in this time unit
        :return:
        """
        # update the total number processed in this current time
        if self.contains(creation_time):
            self.total += slots - self.record[creation_time]
        else:
            self.total += slots

        self.record[creation_time] = slots

    def contains(self, arrival: int) -> bool:
        """
        Indicates whether or not an arrival
        
        :param arrival: the creation time id of the arrival (as a time unit)
        :return: Whether or not an arrival
        """
        return arrival in self.record


class ScheduleResult:
    """
    Properties
    ----------
    schedule: List[TimeUnitBreakdown]
        The number history report on how arrivals were processed and when
    remainder_queue: deque
        The queue of unprocessed arrivals
    """
    def __init__(self, schedule_results: List[TimeUnitBreakdown], remainder_queue: deque):
        self.schedule: List[TimeUnitBreakdown] = schedule_results
        self.remainder_queue = remainder_queue


class AllocationResult:
    """
    Properties
    ----------
    allocation: int
        The number of slots to allocate for each time unit in the interval
    remainder_queue: deque
        The queue of unprocessed arrivals
    """
    def __init__(self, allocation: int, remainder_queue: deque):
        self.allocation = allocation
        self.remainder_queue = remainder_queue
