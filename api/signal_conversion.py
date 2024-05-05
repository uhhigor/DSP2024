import numpy as np

from api.analog_signal import ContinuousSignal, DiscreteSignal


# S1 - próbkowanie równomierne sygnału ciągłego
def uniform_sampling(signal: ContinuousSignal, sampling_rate, time_start, time_end):
    time = np.arange(time_start, time_end, 1 / sampling_rate)
    samples = [signal(t) for t in time]
    return time, samples


def discrete_sampling(signal: DiscreteSignal, samples_num):
    samples_numbers = [n for n in range(samples_num)]
    samples = [signal(n) for n in samples_numbers]
    return samples_numbers, samples


# Q2 - kwantyzacja równomierna z zaokrągleniem
def uniform_quantization(samples: []) -> []:
    return [np.round(sample) for sample in samples]


# R1 - ekstrapolacja zerowego rzędu
def zero_order_extrapolation(samples: []) -> []:
    I1 = np.ones(len(samples), float)
    result = np.convolve(samples, I1, mode='same')
    h = [1 / 33] * 33
    result = np.convolve(result, h, mode='same')
    return result


# R2 - ekstrapolacja pierwszego rzędu
def first_order_extrapolation(samples: []) -> []:
    I2 = np.zeros(2 * len(samples), float)
    for i in range(len(samples)):
        I2[i] = (1 / len(samples)) * i
        I2[i + len(samples)] = 1 - (1 / len(samples)) * i
    result = np.convolve(samples, I2, mode='same')
    h = [1 / 33] * 33
    result = np.convolve(result, h, mode='same')
    return result


# R3 - ekstrapolacja sinc
def sinc_extrapolation(samples: []) -> []:
    I3 = np.zeros(len(samples), float)
    for i in range(len(samples)):
        t = (len(samples) // 2 - i) / len(samples)
        if t == 0:
            v = 1
        else:
            v = np.sin(np.pi * t) / (np.pi * t)
        I3[i] = v

    result = np.convolve(samples, I3, mode='same')
    h = [1 / 33] * 33
    result = np.convolve(result, h, mode='same')
    return result
