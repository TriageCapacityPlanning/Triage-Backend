from .types import ScheduleResult, TimeUnitBreakdown
from collections import deque
from copy import deepcopy
from typing import List


def simulate_allocations(
        arrivals: List[int], slot_schedule: List[int], offset: int,
        current_queue: deque = deque()
) -> ScheduleResult:
    """
    Simulate the proposed schedule and return the processing results of each arrival.

    :param arrivals: the arrivals per unit time, starting at a time relative to the interval
    :param slot_schedule: The amount of slots to allocate per unit time to process arrivals
    :param offset: the relative starting time of the simulation as an int time unit
    :param current_queue: the arrivals that need to be processed
    :return: The details of when each arrival was processed
    """
    if len(arrivals) > len(slot_schedule):
        raise Exception('The slot schedule should have an entry for each arrival to be simulated')
    # the queue will be manipulated throughout the simulation
    # make copy so can reuse the original queue for other simulations with same start
    queue = deepcopy(current_queue)
    allocations: List[TimeUnitBreakdown] = []
    # simulate the slot schedule given over the arrivals
    for rel_time in range(len(slot_schedule)):
        arrival_time = rel_time + offset
        # schedule can be longer than the actual arrivals due to carryovers
        if rel_time < len(arrivals) and arrivals[rel_time] != 0:
            # queue all new nonzero arrivals no matter what, ONCE. Store in format [creation time, slots]
            queue.append([arrival_time, arrivals[rel_time]])
        capacity = slot_schedule[rel_time]
        current_allocation_breakdown = _process_available(queue, capacity, arrival_time)
        # add current allocation to the total schedule sequence
        allocations.append(current_allocation_breakdown)

    allocation_results = ScheduleResult(allocations, queue)
    return allocation_results


def _process_available(queue: deque, capacity: int, time_id: int) -> TimeUnitBreakdown:
    """
    Process as many queue items as possible (cannot exceed max slots allowed) in this time unit.
    Otherwise, leave queue elements to be processed for next time unit.
    Updates queue so that it only contains items that needs to be processed

    :param queue: the arrivals that need to be processed
    :param capacity: the max number of arrivals that can be processed
    :param time_id: the current time when processing the arrivals
    :return: the details of how arrivals were processed at a specific time
    """
    allocation_breakdown: TimeUnitBreakdown = TimeUnitBreakdown(time_id)
    while len(queue) > 0 and allocation_breakdown.total < capacity:
        top = queue[0]
        (top_time, top_arrivals) = top
        # process what you can: either the max slots or all the current and previous queue elements
        if top_arrivals + allocation_breakdown.total > capacity:
            # don't dequeue because it will need to cascade to next iteration
            processable = capacity - allocation_breakdown.total
            top[1] -= processable
            allocation_breakdown.add(top_time, processable)
        else:
            # process everything that can
            last_processed = queue.popleft()
            (creation_time, slots) = last_processed
            # if slots is 0 it does not increase the total slots allocated count
            # (although 0 items should not be in the queue)
            allocation_breakdown.add(creation_time, slots)
    return allocation_breakdown
