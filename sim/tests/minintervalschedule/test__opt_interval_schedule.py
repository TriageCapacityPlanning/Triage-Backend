from sim.resources import minintervalschedule as gas
from collections import deque
import numpy as np

# mock data frame whereby the sample generated is the same per iteration of simulation run
# (makes it easier/more consistent for debugging tests since the N* calculating arrivals are the same as
# the corresponding remainder queue arrivals)
class DataFrame:
    def __init__(self, arrivals, intervals, num_sim_runs):
        self.intervals = intervals
        self.arrivals = arrivals
        self.invoke_count = 0
        self.num_sim_runs = num_sim_runs

    def get_interval_size(self, interval):
        # Check validity of input interval index.
        if interval not in range(0, len(self.intervals)):
            raise ValueError("Invalid interval %s.", interval)

        # Return the length of a given interval
        return self.intervals[interval][1] - self.intervals[interval][0]
    
    def get_interval_sample(self, interval):
        # Check validity of input interval index.
        if interval not in range(0, len(self.intervals)):
            raise ValueError("Invalid interval %s.", interval)
        
        # Get start and end of interval
        start = self.intervals[interval][0]
        end = self.intervals[interval][1]
        
        # Generate and return sample
        mock_rand_variance = 1
        res = [mock_rand_variance * self.invoke_count + a for a in self.arrivals[start:end]]
        print('arrivals: ', res)
        self.invoke_count += 1
        if self.invoke_count >= self.num_sim_runs: self.invoke_count = 0 
        return res


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

def test_confidence():
    # CAREFUL WITH EDITING THIS TEST
    # check the queue for a single sim run for a particular schedule
    queue = deque()
    min_ratio = 0.8
    window = 0.
    final_window = 2.
    num_sim_runs = 1
    confidence = 90
    data_frame = DataFrame([13, 15, 4, 8, 6, 4, 5, 7, 7], [(0, 2), (2, 4), (4, 7), (7, 9)], num_sim_runs)
    schedule1 = gas._opt_interval_schedule(queue=queue, data_frame=data_frame, interval=0, min_ratio=min_ratio,
                                           window=window, final_window=final_window, num_sim_runs=num_sim_runs,
                                           confidence=confidence)
    assert len(schedule1.remainder_queue) == 1
    assert schedule1.remainder_queue[0] == [1, 4]

    # test for multiple sim runs
    # CAREFUL with test!!! Variance is calculated based on num of sim runs
    queue = deque()
    min_ratio = 0.8
    window = 0.
    final_window = 2.
    num_sim_runs = 6
    confidence = 90
    data_frame = DataFrame([9, 11, 4, 8, 6, 4, 5, 7, 7], [(0, 2), (2, 4), (4, 7), (7, 9)], num_sim_runs)
    schedule1 = gas._opt_interval_schedule(queue=queue, data_frame=data_frame, interval=0, min_ratio=min_ratio,
                                           window=window, final_window=final_window, num_sim_runs=num_sim_runs,
                                           confidence=confidence)
    assert len(schedule1.remainder_queue) == 1
    assert schedule1.remainder_queue[0] == [1, 4]

    # LOW CONFIDENCE
    queue = deque()
    min_ratio = 0.8
    window = 0.
    final_window = 2.
    num_sim_runs = 6
    confidence = 50
    data_frame = DataFrame([9, 11, 4, 8, 6, 4, 5, 7, 7], [(0, 2), (2, 4), (4, 7), (7, 9)], num_sim_runs)
    schedule1 = gas._opt_interval_schedule(queue=queue, data_frame=data_frame, interval=0, min_ratio=min_ratio,
                                           window=window, final_window=final_window, num_sim_runs=num_sim_runs,
                                           confidence=confidence)
    assert len(schedule1.remainder_queue) == 1
    assert schedule1.remainder_queue[0] == [1, 2]


