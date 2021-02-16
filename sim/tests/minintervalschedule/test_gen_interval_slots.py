from sim.resources.minintervalschedule import gen_min_interval_slots, DataFrame
from collections import deque
import pytest


def test_returns_schedule():
    queue = deque()
    data_frame = DataFrame([5, 7, 4, 8, 6, 4, 5, 7, 7], [(0, 2), (2, 4), (4, 7), (7, 9)])
    min_ratio = 0.8
    window = 1.
    final_window = 2.
    num_sim_runs = 2
    confidence = 90
    slots = gen_min_interval_slots(queue=queue, data_frame=data_frame, start=1, end=2, min_ratio=min_ratio,
                                   window=window, final_window=final_window, num_sim_runs=num_sim_runs,
                                   confidence=confidence)
    assert len(slots) == 2
    assert slots[0].expected_slots == 5
    assert slots[0].interval_range == (2, 4)
    assert slots[1].expected_slots == 6
    assert slots[1].interval_range == (4, 7)


def test_no_schedule_when_sim_runs_is_0():
    queue = deque()
    data_frame = DataFrame([5, 7, 4, 8, 6, 4, 5, 7, 7], [(0, 2), (2, 4), (4, 7), (7, 9)])
    min_ratio = 0.8
    window = 1.
    final_window = 2.
    num_sim_runs = 0
    confidence = 90

    with pytest.raises(ValueError) as e:
        gen_min_interval_slots(queue=queue, data_frame=data_frame, start=0, end=2, min_ratio=min_ratio,
                               window=window, final_window=final_window, num_sim_runs=num_sim_runs,
                               confidence=confidence)
        assert e is not None


def test_none_when_schedule_infeasible():
    queue = deque([[-10, 1]])
    data_frame = DataFrame([5, 7, 4, 8, 6, 4, 5, 7, 7], [(0, 2), (2, 4), (4, 7), (7, 9)])
    min_ratio = 0.8
    window = 1.
    final_window = 2.
    num_sim_runs = 1
    confidence = 90
    slots = gen_min_interval_slots(queue=queue, data_frame=data_frame, start=0, end=2, min_ratio=min_ratio,
                                   window=window, final_window=final_window, num_sim_runs=num_sim_runs,
                                   confidence=confidence)
    assert slots is None


@pytest.mark.stress
def test_succeeds_when_thousands_of_sims_are_ran():
    queue = deque()
    data_frame = DataFrame([5, 7, 4, 8, 6, 4, 5, 7, 7], [(0, 2), (2, 4), (4, 7), (7, 9)])
    min_ratio = 0.8
    window = 1.
    final_window = 2.
    num_sim_runs = 10000
    confidence = 90
    slots = gen_min_interval_slots(queue=queue, data_frame=data_frame, start=1, end=2, min_ratio=min_ratio,
                                   window=window, final_window=final_window, num_sim_runs=num_sim_runs,
                                   confidence=confidence)
    assert len(slots) == 2
    assert slots[0].expected_slots == 5
    assert slots[0].interval_range == (2, 4)
    assert slots[1].expected_slots == 6
    assert slots[1].interval_range == (4, 7)


@pytest.mark.stress
def test_succeeds_when_hundreds_thousands_arrivals():
    queue = deque()
    arrivals = [5]*100000
    data_frame = DataFrame(arrivals, [(0, len(arrivals))])
    min_ratio = 0.8
    window = 1.
    final_window = 2.
    num_sim_runs = 1
    confidence = 90
    slots = gen_min_interval_slots(queue=queue, data_frame=data_frame, start=0, end=0, min_ratio=min_ratio,
                                   window=window, final_window=final_window, num_sim_runs=num_sim_runs,
                                   confidence=confidence)
    assert len(slots) == 1
    assert slots[0].expected_slots == 5
    assert slots[0].interval_range == (0, len(arrivals))


@pytest.mark.stress
def test_succeeds_when_thousands_arrivals_hundreds_sim_runs():
    queue = deque()
    arrivals = [5]*5000
    data_frame = DataFrame(arrivals, [(0, len(arrivals))])
    min_ratio = 0.8
    window = 1.
    final_window = 2.
    num_sim_runs = 500
    confidence = 90
    slots = gen_min_interval_slots(queue=queue, data_frame=data_frame, start=0, end=0, min_ratio=min_ratio,
                                   window=window, final_window=final_window, num_sim_runs=num_sim_runs,
                                   confidence=confidence)
    assert len(slots) == 1
    assert slots[0].expected_slots == 5
    assert slots[0].interval_range == (0, len(arrivals))
