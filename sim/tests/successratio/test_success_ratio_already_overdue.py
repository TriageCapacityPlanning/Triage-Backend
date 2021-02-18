from sim.resources.success_ratio import success_ratio_already_overdue
from sim.resources import types
from collections import deque
import numpy as np


def test_overdue_success_ratio_succeeds_when_empty_queue():
    breakdown_allocations = []
    queue = deque()
    current_time = 6
    carryover_queue = deque()
    breakdown_6 = types.TimeUnitBreakdown(current_time)
    breakdown_6.add(6, 10)
    breakdown_6.add(5, 10)
    breakdown_6.add(4, 10)
    breakdown_6.add(3, 10)
    breakdown_allocations.append(breakdown_6)
    s = success_ratio_already_overdue(breakdown_allocations, queue, carryover_queue, 6., 6., current_time)
    assert s == 1.


def test_success_ratio_fails_when_queue_contains_already_failed():
    breakdown_allocations = []
    current_time = 6
    queue = deque([[3, 10], [4, 10], [5, 10]])
    carryover_queue = deque()
    breakdown_6 = types.TimeUnitBreakdown(current_time)
    breakdown_6.add(6, 10)
    breakdown_6.add(5, 10)
    breakdown_6.add(4, 10)
    breakdown_6.add(3, 10)
    breakdown_allocations.append(breakdown_6)
    s = success_ratio_already_overdue(breakdown_allocations, queue, carryover_queue, 0., 1., current_time)
    np.testing.assert_almost_equal(s, (10 / (3*10)), decimal=8)


def test_overdue_success_ratio_fails_when_overdue_is_in_carryover():
    # when none of the already overdue queued items are processed there is a 0 success
    breakdown_allocations = []
    current_time = 6
    start_queue = deque([[0, 3], [1, 4]])
    carryover_queue = deque([[0, 3], [1, 4]])
    breakdown_6 = types.TimeUnitBreakdown(current_time)
    breakdown_allocations.append(breakdown_6)
    s = success_ratio_already_overdue(breakdown_allocations, start_queue, carryover_queue, 1., 1., current_time)
    assert s == 0


def test_overdue_success_ratio_100_when_all_processed_before_final():
    # when all already overdue queued items are fully processed before the final window it succeeds
    breakdown_allocations = []
    current_time = 2
    start_queue = deque([[0, 3], [1, 4]])
    carryover_queue = deque()
    breakdown_6 = types.TimeUnitBreakdown(current_time)
    breakdown_6.add(0, 3)
    breakdown_6.add(1, 4)
    breakdown_allocations.append(breakdown_6)
    s = success_ratio_already_overdue(breakdown_allocations, start_queue, carryover_queue, 1., 3., current_time)
    assert s == 1.

    # when all already overdue queued items are fully processed before the final window it succeeds
    # AND other items are processed
    breakdown_allocations = []
    current_time = 2
    start_queue = deque([[0, 3], [1, 4]])
    carryover_queue = deque()
    breakdown_6 = types.TimeUnitBreakdown(current_time)
    breakdown_6.add(0, 3)
    breakdown_6.add(1, 4)
    breakdown_6.add(2, 4)
    breakdown_allocations.append(breakdown_6)
    s = success_ratio_already_overdue(breakdown_allocations, start_queue, carryover_queue, 1., 3., current_time)
    assert s == 1.


def test_overdue_success_ratio_partially_succeeds_when_partial_processed_before_final():
    # when some already overdue queued items are fully processed before the final window not all succeed
    breakdown_allocations = []
    current_time = 2
    start_queue = deque([[0, 3], [1, 4]])
    carryover_queue = deque()
    breakdown_6 = types.TimeUnitBreakdown(current_time)
    breakdown_6.add(0, 3)
    breakdown_6.add(1, 4)
    breakdown_allocations.append(breakdown_6)
    s = success_ratio_already_overdue(breakdown_allocations, start_queue, carryover_queue, 0., 1., current_time)
    assert s == 4/7
