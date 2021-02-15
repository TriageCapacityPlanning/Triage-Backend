from sim import simulate_allocations
import pytest


def test_errors_when_arrivals_and_schedule_diff_len():
    with pytest.raises(Exception):
        arrivals = [100, 200, 300]
        simulate_allocations(arrivals, [100], 0)
    with pytest.raises(Exception):
        simulate_allocations([100], [], 0)
    with pytest.raises(Exception):
        arrivals = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        simulate_allocations(arrivals, [], 0)


def test_allocations_do_not_exceed_arrivals():
    """
    When the suggested schedule allocates at least as many slots than there are arrivals,
    validate that there is no carryover and also that there is each allocation
    does not exceed the amount of arrivals
    :return:
    """
    # the actual allocation does not exceed the arrivals
    arrivals = [10, 10, 10]
    overzealous_schedule = simulate_allocations(arrivals, [1000000, 1000000, 1000000], 0)
    assert overzealous_schedule.schedule[0].total == 10
    assert overzealous_schedule.schedule[1].total == 10
    assert overzealous_schedule.schedule[2].total == 10
    assert len(overzealous_schedule.schedule) == 3
    arrivals = [10, 10, 10]
    exact_schedule = simulate_allocations(arrivals, [10, 10, 10], 0)
    assert exact_schedule.schedule[0].total == 10
    assert exact_schedule.schedule[1].total == 10
    assert exact_schedule.schedule[2].total == 10
    assert len(exact_schedule.schedule) == 3

    # for all carryovers, the allocation does not exceed the maximum slots allowed in the allocation schedule
    arrivals = [10, 10, 10]
    schedule_with_carryover = simulate_allocations(arrivals, [8, 8, 8, 8], 0)
    assert schedule_with_carryover.schedule[0].total == 8
    assert schedule_with_carryover.schedule[1].total == 8
    assert schedule_with_carryover.schedule[2].total == 8
    assert schedule_with_carryover.schedule[3].total == 6
    assert len(schedule_with_carryover.schedule) == 4


def test_fills_schedule_completely_and_nonzero_carryover_is_correct():
    """
    When the schedule is filled completely, validate that there are nonzero carry overs happen when the schedule doesn't
    serve all the arrivals.
    :return:
    """
    arrivals = [10, 10, 10]
    schedule_same_length_as_arrivals = simulate_allocations(arrivals, [10, 10, 9], 0)
    assert schedule_same_length_as_arrivals.schedule[0].total == 10
    assert schedule_same_length_as_arrivals.schedule[1].total == 10
    assert schedule_same_length_as_arrivals.schedule[2].total == 9
    assert len(schedule_same_length_as_arrivals.schedule) == 3

    arrivals = [10, 10, 10]
    schedule_longer_than_arrivals = simulate_allocations(arrivals, [5, 5, 5, 5, 5, 4], 0)
    assert schedule_longer_than_arrivals.schedule[0].total == 5
    assert schedule_longer_than_arrivals.schedule[1].total == 5
    assert schedule_longer_than_arrivals.schedule[2].total == 5
    assert schedule_longer_than_arrivals.schedule[3].total == 5
    assert schedule_longer_than_arrivals.schedule[4].total == 5
    assert schedule_longer_than_arrivals.schedule[5].total == 4
    assert len(schedule_longer_than_arrivals.schedule) == 6

    # the schedule is way too low and has a really large carryover
    arrivals = [1000000, 1000000, 1000000]
    schedule_large_remainder = simulate_allocations(arrivals, [1, 1, 1], 0)
    assert schedule_large_remainder.schedule[0].total == 1
    assert schedule_large_remainder.schedule[1].total == 1
    assert schedule_large_remainder.schedule[2].total == 1
    assert len(schedule_large_remainder.schedule) == 3


def test_schedule_of_equal_length_to_arrivals():
    """
    When the schedule is filled exactly, there is no carry over and no other slots days created
    :return:
    """
    # allocation schedule provided is the same size as the arrivals dates
    arrivals = [10, 10, 10]
    schedule_same_length_as_arrivals = simulate_allocations(arrivals, [10, 10, 10], 0)
    assert schedule_same_length_as_arrivals.schedule[0].total == 10
    assert schedule_same_length_as_arrivals.schedule[1].total == 10
    assert schedule_same_length_as_arrivals.schedule[2].total == 10
    assert len(schedule_same_length_as_arrivals.schedule) == 3


def test_schedule_greater_length_and_capacity_to_arrivals():
    """
    When the schedule has an overzealous capacity and also has sufficient size,
    validate that the schedule of slots allocated is at most the size of the suggested allocation.
    All trailing 0 entries are sliced off
    :return:
    """
    # allocation schedule is larger than the actual schedule used up
    arrivals = [10, 10, 10]
    schedule_same_length_as_arrivals = simulate_allocations(arrivals, [10, 10, 10, 10], 0)
    assert schedule_same_length_as_arrivals.schedule[0].total == 10
    assert schedule_same_length_as_arrivals.schedule[1].total == 10
    assert schedule_same_length_as_arrivals.schedule[2].total == 10
    assert schedule_same_length_as_arrivals.schedule[3].total == 0
    assert len(schedule_same_length_as_arrivals.schedule) == 4


def test_offset_applied_to_all_arrival_times():
    """
    When the schedule has an overzealous capacity and also has sufficient size,
    validate that the schedule of slots allocated is at most the size of the suggested allocation.
    All trailing 0 entries are sliced off
    :return:
    """
    # allocation schedule is larger than the actual schedule used up
    arrivals = [10, 10, 10]
    schedule_same_length_as_arrivals = simulate_allocations(arrivals, [10, 10, 10], 2)
    assert True, schedule_same_length_as_arrivals.schedule[0].contains(2)
    assert True, schedule_same_length_as_arrivals.schedule[1].contains(3)
    assert True, schedule_same_length_as_arrivals.schedule[2].contains(4)
