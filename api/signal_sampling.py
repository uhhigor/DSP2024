import numpy as np

from api.analog_signal import ContinousSignal, DiscreteSignal


def uniform_sampling(signal: ContinousSignal, sampling_rate, time_start, time_end):
    time = np.arange(time_start, time_end, 1 / sampling_rate)
    samples = [signal(t) for t in time]
    return time, samples


def discrete_sampling(signal: DiscreteSignal, samples_num):
    samples_numbers = [n for n in range(samples_num)]
    samples = [signal(n) for n in samples_numbers]
    return samples_numbers, samples
