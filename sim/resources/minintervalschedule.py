from collections import deque
from .types import AllocationResult
from .simulateallocations import simulate_allocations
import numpy as np
from typing import List, Tuple, Union
import math
from .success_ratio import success_ratio, success_ratio_already_overdue
from api.common.controller.DataFrame import DataFrame


# temp mock up datatype
'''class DataFrame:
    def __init__(self, data: List[int], intervals: List[Tuple[int, int]]):
        self.data = data
        self.intervals = intervals

    def get_interval_sample(self, i: int):
        start, end = self.intervals[i]
        return self.data[start: end]

    def get_interval_size(self, i: int):
        start, end = self.intervals[i]
        return end - start'''


class SimulationResults:
    """ Get the optimal patient allocation to slots
    Properties
    ----------
    expected_slots : float
        The expected number of minimum slots needed calculated from the simulation
    interval_range : Tuple[int, int]
        The relative date range of that the expected slot corresponds to

    """
    def __init__(self, expected_slots: float, interval_range: Tuple[int, int]):
        self.expected_slots = expected_slots
        self.interval_range = interval_range


def gen_min_interval_slots(data_frame: DataFrame, window: float, min_ratio: float, final_window: float,
                           confidence: float, start: int, end: int, num_sim_runs: int = 1000,
                           queue: deque = None) -> Union[None, List[SimulationResults]]:
    """
    Get the optimal patient schedule.
    Throws an error if num sim runs is <= 0

    :param data_frame: Stochastic arrivals generator
    :param window: the time in which an arrival must be processed by, and if not is considered overdue.
           Must correspond to the same time unit as the rate of arrivals time.
    :param min_ratio: The minimum percentage of arrivals that must be processed throughout the simulation within the
           corresponding time window
    :param final_window: the time in which 100% of arrival must be processed by. Must correspond to the same time unit
           as the rate of arrivals time
    :param confidence: The level of statistical confidence to calculate the margin of error results on
    :param start: The index of the first interval
    :param end: The index of the end of the last relevant interval
    :param num_sim_runs: The number of times to run the simulation > 0
    :param queue: The number of priority elements to process (must be processed before newer arrivals)
    :return: the results of the simulation, or None if schedule is infeasible
    """

    if num_sim_runs <= 0:
        raise ValueError('Invalid simulation run value specified')

    if final_window < window or min_ratio == 1.:
        raise ValueError('Invalid final window and window value supplied')

    expected_slots: List[SimulationResults] = []
    # simulate each interval
    for interval in range(len(data_frame.intervals)):
        interval_schedule = _opt_interval_schedule(queue=queue, data_frame=data_frame, interval=interval,
                                                   min_ratio=min_ratio, window=window, final_window=final_window,
                                                   num_sim_runs=num_sim_runs, confidence=confidence)
        # only occurs when the very first start queue contains arrivals past the final deadline
        if not interval_schedule:
            return None
        sim_result = SimulationResults(interval_schedule.allocation, data_frame.intervals[interval])
        expected_slots.append(sim_result)
        queue = interval_schedule.remainder_queue
    relevant_expected_slots = expected_slots[start:end + 1]
    return relevant_expected_slots


def _opt_interval_schedule(queue: deque, data_frame: DataFrame, interval: int, min_ratio: float,
                           window: float, final_window: float, num_sim_runs: int, confidence: float)\
        -> Union[AllocationResult, None]:
    """
    Get the optimal schedule for a specific interval

    :param queue: the queue of arrivals before this interval start time
    :param data_frame: an object which generates stochastic arrivals per unit time, starting at a time relative to the
           interval
    :param interval: the interval time
    :param min_ratio: the minimum rate at which arrivals must be processed at
    :param window: the time in which an arrival must be processed by, and if not is considered overdue.
    :param final_window: the time in which 100% of arrival must be processed by. Must correspond to the same time unit
           as the rate of arrivals time
    :param num_sim_runs: the number of times in which to run the simulation
    :param confidence: the level of confidence in which the stochastic optimum is calculated in
    :return: the optimal allocation for the interval
    """
    allocations: List[int] = []
    offset = data_frame.intervals[interval][0]
    for _ in range(num_sim_runs):
        stochastic_arrivals = data_frame.get_interval_sample(interval)
        hi = _hi(queue, stochastic_arrivals)
        allocation = _min_uniform_allocation(arrivals=stochastic_arrivals, queue=queue, offset=offset,
                                             min_ratio=min_ratio, window=window, final_window=final_window,
                                             lo=0, hi=hi)
        # if no schedule was found
        # only occurs when the starting queue contains arrivals past the final deadline
        if allocation is None:
            return None
        allocations.append(allocation)
    # calculate the resulting queue for N*
    opt = math.ceil(np.percentile(allocations, confidence))
    sample_arrival = data_frame.get_interval_sample(interval)
    schedule_with_padding = _gen_uniform_suggested_schedule(arrivals=sample_arrival, allocation_amount=opt, window=window)

    interval_size_schedule = schedule_with_padding[:data_frame.get_interval_size(interval)]
    schedule_sim_result = simulate_allocations(arrivals=sample_arrival, slot_schedule=interval_size_schedule,
                                               current_queue=queue, offset=offset)
    opt_allocation = AllocationResult(opt, schedule_sim_result.remainder_queue)
    return opt_allocation


def _gen_uniform_suggested_schedule(arrivals: List[int], allocation_amount: int, window: float) \
        -> List[int]:
    """
    Generate the uniform schedule for all the arrivals.
    Also padded with allocations at the end to assign processing times to the end arrivals.

    :param arrivals: the arrivals per unit time, starting at a time relative to the interval
    :param allocation_amount: the amount of slots to allocate
    :param window: the time in which an arrival must be processed by, and if not is considered overdue.
           Must correspond to the same time unit as the rate of arrivals time.
    :return: a schedule with sufficient padding
    """
    max_time_to_process_last_arrivals = math.ceil(window * 2)
    return [allocation_amount] * (len(arrivals) + max_time_to_process_last_arrivals)


def _min_uniform_allocation(queue: deque, arrivals: List[int], min_ratio: float, window: float, final_window: float,
                            offset: int, lo: int, hi: int) -> Union[int, None]:
    """
    Binary search for the minimum uniform allocation (all allocations are equal) of quantity n
    that processes AT LEAST the min ratio of arrivals within the window. Returns none if there does not exist a schedule
    in which arrivals are processed by the final window

    :param queue: the queue of arrivals before this interval start time
    :param arrivals: the arrivals per unit time, starting at a time (time = 0) relative to the interval
    :param min_ratio: the minimum rate at which arrivals must be processed at
    :param window: the time in which an arrival must be processed by, and if not is considered overdue.
           Must correspond to the same time unit as the rate of arrivals time.
    :param final_window: the time in which 100% of arrival must be processed by. Must correspond to the same time unit
           as the rate of arrivals time
    :param offset: the relative starting time of the simulation in the as an int time unit
    :param lo: the search minimum
    :param hi: the search upper bound
    :return: a number of slots that returns a feasible schedule given the processing constraints
    """
    lowest_alloc = float('inf')
    while lo <= hi:
        mid = (lo + hi) // 2
        schedule = _gen_uniform_suggested_schedule(arrivals=arrivals, allocation_amount=mid, window=window)
        sim_result = simulate_allocations(arrivals=arrivals, slot_schedule=schedule,
                                          current_queue=queue, offset=offset)
        success_rate = success_ratio(sim_result.schedule, queue, sim_result.remainder_queue, window, offset)
        processed_all_already_overdue = success_ratio_already_overdue(sim_result.schedule, queue,
                                                                      sim_result.remainder_queue, window, final_window,
                                                                      offset) == 1

        # update the min feasible value
        if success_rate >= min_ratio and processed_all_already_overdue and mid < lowest_alloc:
            lowest_alloc = mid

        ratio_eq_100_and_success = (not _exists_gap(schedule, arrivals) and min_ratio == 1 and success_rate == 1
                                    and processed_all_already_overdue)

        ratio_lt_100_and_success = (min_ratio < 1. and success_rate == min_ratio < 1. and processed_all_already_overdue)

        # search until we have minimized the feasible value we can go
        if ratio_lt_100_and_success or ratio_eq_100_and_success or (lo == hi and lowest_alloc < float('inf')):
            return lowest_alloc

        ratio_is_100_and_fail = (_exists_gap(schedule, arrivals) and success_rate == min_ratio
                                 and processed_all_already_overdue)
        ratio_lt_100_and_minimizable = (success_rate > min_ratio and processed_all_already_overdue)
        if ratio_is_100_and_fail or ratio_lt_100_and_minimizable:
            hi = mid
        else:
            lo = mid + 1
    return None


def _hi(queue: deque, arrivals: List[int]):
    """
    Calculate the search upper bound

    :param queue: the arrivals that need to be processed going into the simulation
    :param arrivals: the arrivals that occur throughout the simulation per unit time
    :return: the maximum number of slots that will ensure 100% of patients are seen on time unit 1.
    """
    previous_arrivals: List[int] = []
    for _, arrival_count in queue:
        previous_arrivals.append(arrival_count)
    # let the search ceiling be the larger of the sum of all previous arrivals
    # if the previous arrival queue is empty then the schedule that allocates the max arrival each
    # time unit is guaranteed to process 100% within one time unit
    # else if previous queue is not empty, then processing all previous arrivals in one day + the
    # max of any current arrivals guarantees that we process 100% the previous + current within
    # one time unit
    return sum(previous_arrivals) + max(arrivals)


def _exists_gap(schedule: List[int], arrivals: List[int]):
    """
    Determines whether or not there are slot allocations that equal the number of arrivals in that time unit

    :param schedule: the slots allocated per time unit
    :param arrivals:the arrivals per unit time
    :return: Whether or not there exists a slot allocation equal to the number of arrivas
    """
    # schedule should be at least as long as arrivals (due to arrival carryovers)
    for i in range(len(arrivals)):
        if arrivals[i] == schedule[i]:
            return False
    return True
