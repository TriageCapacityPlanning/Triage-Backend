from sim.resources.success_ratio import success_ratio
from sim.resources import types
import numpy as np
from collections import deque


def test_success_ratio_out_of_scope_start_queue():
    # Validate that arrivals already expired are not counted in the success ratio
    breakdown_allocations = []
    current_time = 6
    start_queue = deque([[3, 10], [4, 10], [5, 10]])
    carryover_queue = deque()
    breakdown_6 = types.TimeUnitBreakdown(current_time)
    breakdown_6.add(6, 10)
    breakdown_6.add(5, 10)
    breakdown_6.add(4, 10)
    breakdown_6.add(3, 10)
    breakdown_allocations.append(breakdown_6)
    s = success_ratio(breakdown_allocations, start_queue, carryover_queue,  2., current_time)
    assert s == 1.


def test_success_ratio_partial():
    # Validate that arrivals already expired are not counted in the success ratio
    breakdown_allocations = []
    current_time = 6
    sim_start_time = 2
    start_queue = deque([[3, 10], [4, 10], [5, 10]])
    carryover_queue = deque()
    breakdown_6 = types.TimeUnitBreakdown(current_time)
    breakdown_6.add(6, 10)
    breakdown_6.add(5, 10)
    breakdown_6.add(4, 10)
    breakdown_6.add(3, 10)
    breakdown_allocations.append(breakdown_6)
    s = success_ratio(breakdown_allocations, start_queue, carryover_queue,  2., sim_start_time)
    assert s == (10 * 3) / (10 * 4)


def test_success_ratio_100_already_expired_ignored():
    # Validate that arrivals already expired are not counted in the success ratio
    breakdown_allocations = []
    current_time = 6
    sim_start_time = 6
    start_queue = deque([[3, 10]])
    carryover_queue = deque()
    breakdown_6 = types.TimeUnitBreakdown(current_time)
    breakdown_6.add(3, 10)
    breakdown_allocations.append(breakdown_6)
    s = success_ratio(breakdown_allocations, start_queue, carryover_queue,  2., sim_start_time)
    assert s == (10 * 3) / (10 * 3)


def test_success_ratio_100_empty_start_queue():
    # Validate that arrivals already expired are not counted in the success ratio
    breakdown_allocations = []
    current_time = 6
    sim_start_time = 2
    start_queue = deque()
    carryover_queue = deque()
    breakdown_6 = types.TimeUnitBreakdown(current_time)
    breakdown_6.add(6, 10)
    breakdown_allocations.append(breakdown_6)
    s = success_ratio(breakdown_allocations, start_queue, carryover_queue,  2., sim_start_time)
    assert s == 1.


def test_success_ratio_100_empty_start_queue_empty_schedule():
    # Validate that arrivals already expired are not counted in the success ratio
    breakdown_allocations = []
    current_time = 6
    sim_start_time = 2
    start_queue = deque()
    carryover_queue = deque()
    breakdown_6 = types.TimeUnitBreakdown(current_time)
    breakdown_allocations.append(breakdown_6)
    s = success_ratio(breakdown_allocations, start_queue, carryover_queue,  2., sim_start_time)
    assert s == 1.


def test_success_ratio_partial_in_scope_start_queue():
    # Validate that arrivals already expired are not counted in the success ratio
    breakdown_allocations = []
    current_time = 6
    sim_start_time = 2
    start_queue = deque([[3, 10], [4, 10], [5, 10]])
    carryover_queue = deque()
    breakdown_6 = types.TimeUnitBreakdown(current_time)
    breakdown_6.add(6, 10)
    breakdown_6.add(5, 10)
    breakdown_6.add(4, 10)
    breakdown_6.add(3, 10)
    breakdown_allocations.append(breakdown_6)
    s = success_ratio(breakdown_allocations, start_queue, carryover_queue,  2., sim_start_time)
    assert s == (10 * 3) / (10 * 4)


def test_success_ratio_0_start_queue():
    # Validate that arrivals already expired are not counted in the success ratio
    breakdown_allocations = []
    current_time = 6
    sim_start_time = 2
    start_queue = deque([[3, 10], [4, 10]])
    carryover_queue = deque()
    breakdown_6 = types.TimeUnitBreakdown(current_time)
    breakdown_6.add(4, 10)
    breakdown_6.add(3, 10)
    breakdown_allocations.append(breakdown_6)
    s = success_ratio(breakdown_allocations, start_queue, carryover_queue,  0., sim_start_time)
    assert s == 0.


def test_success_ratio_partial_multiple_allocations_nonzero_window():
    """
    validate that when another unit allocation is added to the list of allocations
    that the ratio is calculated correctly using both allocations
    :return:
    """
    breakdown_allocations = []
    start_queue = deque([[0, 10], [1, 10]])
    carryover_queue = deque()
    breakdown_2 = types.TimeUnitBreakdown(2)
    breakdown_2.add(2, 10)
    breakdown_2.add(1, 10)
    breakdown_2.add(0, 10)
    breakdown_allocations.append(breakdown_2)
    breakdown_6 = types.TimeUnitBreakdown(6)
    breakdown_6.add(6, 10)
    breakdown_6.add(5, 10)
    breakdown_6.add(4, 10)
    breakdown_6.add(3, 10)
    breakdown_allocations.append(breakdown_6)

    s = success_ratio(breakdown_allocations, start_queue, carryover_queue,  2., 0)
    np.testing.assert_almost_equal(s, (10 * 3 + 10 * 3) / (10 * 3 + 10 * 4), decimal=8)


def test_success_ratio_partial_multiple_allocations_zero_window():
    """
    validate that when another unit allocation is added to the list of allocations
    that the ratio is calculated correctly using both allocations
    :return:
    """
    breakdown_allocations = []
    start_queue = deque([[0, 10], [1, 10]])
    carryover_queue = deque()
    breakdown_2 = types.TimeUnitBreakdown(2)
    breakdown_2.add(1, 10)
    breakdown_2.add(0, 10)
    breakdown_allocations.append(breakdown_2)
    breakdown_3 = types.TimeUnitBreakdown(3)
    breakdown_3.add(3, 10)
    breakdown_3.add(2, 10)
    breakdown_allocations.append(breakdown_3)

    s = success_ratio(breakdown_allocations, start_queue, carryover_queue,  0., 2)
    np.testing.assert_almost_equal(s, (10 / (10*2)), decimal=8)
