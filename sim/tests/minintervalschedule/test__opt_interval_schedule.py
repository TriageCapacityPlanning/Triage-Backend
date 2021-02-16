from sim.resources import minintervalschedule as gas
from collections import deque


def test_creates_correct_remainder():
    queue = deque()
    data_frame = gas.DataFrame([5, 7, 4, 8, 6, 4, 5, 7, 7], [(0, 2), (2, 4), (4, 7), (7, 9)])
    interval = 0
    min_ratio = 0.8
    window = 1.
    final_window = 2.
    num_sim_runs = 2
    confidence = 90
    schedule = gas._opt_interval_schedule(queue=queue, data_frame=data_frame, interval=interval, min_ratio=min_ratio,
                                          window=window, final_window=final_window, num_sim_runs=num_sim_runs,
                                          confidence=confidence)
    assert len(schedule.remainder_queue) == 1
    assert schedule.remainder_queue[0] == [1, 4]


def test_creates_correct_remainder_queue():
    queue = deque([[-10, 20]])
    data_frame = gas.DataFrame([5, 7, 4, 8, 6, 4, 5, 7, 7], [(0, 2), (2, 4), (4, 7), (7, 9)])
    interval = 0
    min_ratio = 0.8
    window = 1.
    final_window = 2.
    num_sim_runs = 2
    confidence = 90
    schedule = gas._opt_interval_schedule(queue=queue, data_frame=data_frame, interval=interval, min_ratio=min_ratio,
                                          window=window, final_window=final_window, num_sim_runs=num_sim_runs,
                                          confidence=confidence)
    assert schedule is None


def test_creates_correct_remainder_queue_after_multiple_intervals():
    queue = deque()
    data_frame = gas.DataFrame([5, 7, 4, 8, 6, 4, 5, 7, 7], [(0, 2), (2, 4), (4, 7), (7, 9)])
    min_ratio = 0.8
    window = 0.
    final_window = 2.
    num_sim_runs = 2
    confidence = 90
    schedule1 = gas._opt_interval_schedule(queue=queue, data_frame=data_frame, interval=0, min_ratio=min_ratio,
                                           window=window, final_window=final_window, num_sim_runs=num_sim_runs,
                                           confidence=confidence)
    assert len(schedule1.remainder_queue) == 1
    assert schedule1.remainder_queue[0] == [1, 2]
    schedule2 = gas._opt_interval_schedule(queue=schedule1.remainder_queue, data_frame=data_frame, interval=1,
                                           min_ratio=min_ratio, window=window, final_window=final_window,
                                           num_sim_runs=num_sim_runs, confidence=confidence)
    assert len(schedule2.remainder_queue) == 1
    assert schedule2.remainder_queue[0] == [3, 2]

