from sim.resources import minintervalschedule as gas
from collections import deque


def test_calculates_min_start_empty_queue_no_arrivals():
    start_queue = deque()
    arrivals = [0, 0, 0]
    allocation = gas._min_uniform_allocation(start_queue, arrivals, 1., 1., 1., 0, 0, len(arrivals))
    assert True, allocation == 0


def test_calculates_min_start_empty_queue_window_1():
    """
    Validate that when the start queue is empty that for varying ratios
    and a deadline of 1 unit time that the entries are all equal
    to the max element
    :return:
    """
    # values are all different and arrivals are small
    start_queue = deque()
    arrivals = [2, 0, 3]
    allocation = gas._min_uniform_allocation(queue=start_queue, arrivals=arrivals, min_ratio=1., window=0.,
                                             final_window=0., offset=0, lo=0, hi=len(arrivals))
    assert allocation == 3

    # values are all the different and arrivals are large
    start_queue = deque()
    arrivals = [2, 0, 3] * 1000
    window = 0.
    allocation = gas._min_uniform_allocation(queue=start_queue, arrivals=arrivals, window=window, min_ratio=1.,
                                             final_window=window, offset=0, lo=0, hi=len(arrivals))
    assert True, allocation == 3

    # values are all the same and arrivals are small
    start_queue = deque()
    arrivals = [1, 1, 1]
    window = 0.
    allocation = gas._min_uniform_allocation(queue=start_queue, arrivals=arrivals, window=window, min_ratio=1.,
                                             final_window=window, offset=0, lo=0, hi=len(arrivals))
    assert allocation == 1


def test_allocates_slots_for_large_list_when_ratio_is_1_window_0():
    # values are all the same and arrivals are large
    start_queue = deque()
    arrivals = [1] * 1000
    window = 0.
    allocation = gas._min_uniform_allocation(queue=start_queue, arrivals=arrivals, window=window, min_ratio=1.,
                                             final_window=window, offset=0, lo=0, hi=len(arrivals))
    assert allocation == 1


def test_no_schedule_when_overdue_arrivals_exceed_final_window():
    # Validate that when 90% of arrivals must be seen immediately and there are arrivals that are already
    # overdue that the algorithm ensures that the not-already overdue items are still seen within their threshold
    start_queue = deque([[-4, 9], [-3, 5], [-2, 1], [-1, 10]])
    # it must process in order 9 -> 5 -> 1 -> 10. The algorithm must ensure that all 10
    # not already overdue arrivals have min of >= 90% processed
    window = 0
    arrivals = [0, 0, 0]
    allocation = gas._min_uniform_allocation(queue=start_queue, arrivals=arrivals, window=window, min_ratio=1.,
                                             final_window=window, offset=0, lo=0, hi=9+5+1+10)
    assert allocation is None


def test_no_schedule_when_hi_too_small():
    # Validate that when 90% of arrivals must be seen immediately and there are arrivals that are already
    # overdue that the algorithm ensures that the not-already overdue items are still seen within their threshold
    start_queue = deque()
    # it must process in order 9 -> 5 -> 1 -> 10. The algorithm must ensure that all 10
    # not already overdue arrivals have min of >= 90% processed
    window = 0
    arrivals = [2, 0, 0]
    allocation = gas._min_uniform_allocation(queue=start_queue, arrivals=arrivals, window=window, min_ratio=1.,
                                             final_window=window, offset=0, lo=0, hi=1)
    assert allocation is None
