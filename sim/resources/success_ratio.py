from .types import (TimeUnitBreakdown)
from typing import List
from collections import deque


def success_ratio(schedule: List[TimeUnitBreakdown], start_queue: deque, carryover_queue: deque, window: float,
                  sim_start_time: int) -> float:
    """
    The success rate at which not already overdue arrivals are processed at

    :param schedule: the details on when each arrival was processed at for an interval where each entry corresponds to
           a time unit relative to the interval start time (which is at time 0).
    :param start_queue: the start of the queue before the set of arrivals were processed
    :param carryover_queue: the resulting queue after all the arrivals were processed for a particular time period
    :param window: the time in which an arrival must be processed by, and if not is considered overdue.
           Must correspond to the same time unit as the rate of arrivals time.
    :param sim_start_time: the relative starting time of the simulation as an int time unit
    :return: the rate at which arrivals were processed at within the time window
    """

    num_became_overdue = _num_became_overdue(schedule, carryover_queue, window, sim_start_time)
    num_already_overdue = _total_already_overdue(start_queue, window, sim_start_time)
    total = _total(schedule, carryover_queue)
    total_not_already_overdue = total - num_already_overdue
    if total_not_already_overdue == 0:
        return 1.

    # single count overdue arrivals
    fail_rate = num_became_overdue / total_not_already_overdue

    success_rate = 1-fail_rate

    return success_rate


def success_ratio_already_overdue(schedule: List[TimeUnitBreakdown], start_queue: deque, carryover_queue: deque,
                                  window: float, final_window: float, sim_start_time: int) -> float:
    """
    The success rate at which already overdue arrivals are processed at

    :param schedule: the details on when each arrival was processed at for an interval where each entry corresponds to
           a time unit relative to the interval start time (which is at time 0).
    :param start_queue: the start of the queue before the set of arrivals were processed
    :param carryover_queue: the resulting queue after all the arrivals were processed for a particular time period
    :param window: the time in which an arrival must be processed by, and if not is considered overdue.
           Must correspond to the same time unit as the rate of arrivals time.
    :param final_window: the time in which 100% of arrival must be processed by. Must correspond to the same time unit
           as the rate of arrivals time
    :param sim_start_time: the relative starting time of the simulation as an int time unit
    :return: the rate at which arrivals were processed at within the time window
    """
    num_overdue_failed = _num_already_overdue_failed(schedule, carryover_queue, final_window, sim_start_time)
    total_already_overdue = _total_already_overdue(start_queue, window, sim_start_time)
    if total_already_overdue == 0:
        return 1.
    fail_rate = num_overdue_failed / total_already_overdue
    success_rate = 1-fail_rate
    return success_rate


def _total(schedule: List[TimeUnitBreakdown], carryover_queue: deque) -> int:
    """
    Calculates the total number of arrivals in this simulation interval

    :param schedule: the details on when each arrival was processed at for an interval where each entry corresponds to
           a time unit relative to the interval start time (which is at time 0).
    :param carryover_queue: the resulting queue after all the arrivals were processed for a particular time period
    :return: The total number of arrivals in this simulation interval
    """
    total = 0
    for unit_time in range(len(schedule)):
        total += schedule[unit_time].total
    # check the carryover queue
    for (_, arrival_count) in carryover_queue:
        total += arrival_count
    return total


def _num_became_overdue(schedule: List[TimeUnitBreakdown], carryover_queue: deque, window: float, sim_start_time: int)\
        -> int:
    """
    Count the number of arrivals that became overdue

    :param schedule: the details on when each arrival was processed at for an interval where each entry corresponds to
           a time unit relative to the interval start time (which is at time 0).
    :param window: the time in which an arrival must be processed by, and if not is considered overdue.
           Must correspond to the same time unit as the rate of arrivals time.
    :param sim_start_time: the relative starting time of the simulation as an int time unit
    :return:
    """
    count = 0
    unit_time = 0
    # check the schedule
    for unit_time in range(len(schedule)):
        for (arrival_time, num_arrivals) in schedule[unit_time].record.items():
            if schedule[unit_time].current_time - arrival_time > window and arrival_time >= sim_start_time-window:
                count += num_arrivals
    # check the carryover queue
    unit_time += 1
    for (arrival_time, arrival_count) in carryover_queue:
        if arrival_time >= sim_start_time-window and unit_time + sim_start_time - arrival_time > window:
            count += arrival_count
    return count


def _total_already_overdue(start_queue: deque, window: float, sim_start_time: int)\
        -> int:
    """
    Gives the number of already overdue processed that arrived to this interval in the start queue

    :param start_queue: the start of the queue before the set of arrivals were processed
    :param window: the time in which an arrival must be processed by, and if not is considered overdue.
           Must correspond to the same time unit as the rate of arrivals time.
    :param sim_start_time: the relative starting time of the simulation as an int time unit
    :return: the number of already overdue processed that arrived to this interval in the start queue
    """
    count = 0
    # check the start of simulation queue
    for (arrival_time, arrival_count) in start_queue:
        if sim_start_time - arrival_time > window:
            count += arrival_count
    return count


def _num_already_overdue_failed(schedule: List[TimeUnitBreakdown], carryover_queue: deque, final_window: float,
                                sim_start_time: int) -> int:
    """
    Gives the number of items that are already overdue and failed to be processed within the final window time

    :param schedule: the details on when each arrival was processed at for an interval where each entry corresponds to
           a time unit relative to the interval start time (which is at time 0).
    :param carryover_queue: the resulting queue after all the arrivals were processed for a particular time period
    :param final_window: the time in which 100% of arrival must be processed by. Must correspond to the same time unit
           as the rate of arrivals time
    :param sim_start_time: the relative starting time of the simulation as an int time unit
    :return: the number of items that are already overdue and failed to be processed within the final window time
    """
    count = 0
    unit_time = 0
    # check the schedule
    for unit_time in range(len(schedule)):
        for (arrival_time, num_arrivals) in schedule[unit_time].record.items():
            if arrival_time < sim_start_time and schedule[unit_time].current_time - arrival_time > final_window:
                count += num_arrivals
    # check the carryover queue
    for (arrival_time, arrival_count) in carryover_queue:
        if sim_start_time + unit_time - arrival_time > final_window:
            count += arrival_count
    return count
