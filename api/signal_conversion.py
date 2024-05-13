import math

import numpy as np

from api.analog_signal import ContinuousAnalogSignal, DiscreteAnalogSignal
from api.digital_signal import DigitalSignal


def uniform_sampling(signal: ContinuousAnalogSignal, sampling_rate, time_start, time_end):
    time = np.arange(time_start, time_end, 1 / sampling_rate)
    samples = [signal(t) for t in time]
    return DigitalSignal(start_time=time_start, sampling_rate=sampling_rate, samples=samples, time=time)


def discrete_sampling(signal: DiscreteAnalogSignal, samples_num) -> DigitalSignal:
    samples_numbers = [n for n in range(samples_num)]
    samples = [signal(n) for n in samples_numbers]
    return DigitalSignal(start_time=0, sampling_rate=1, samples=samples, time=samples_numbers)


# S1 - próbkowanie równomierne sygnału ciągłego
def conversion_sampling(y_values: [], number_of_samples):
    N = len(y_values)
    M = number_of_samples
    L = N // M
    x1 = np.zeros(N, float)
    for i in range(0, M):
        x1[int(i * L)] = y_values[int(i * L)]
    return x1


# Q2 - kwantyzacja równomierna z zaokrągleniem
def uniform_quantization(y_values: []) -> []:
    samples = [np.round(value) for value in y_values]
    return samples


# R1 - ekstrapolacja zerowego rzędu

def zero_order_extrapolation(y_values: [], L: int) -> []:
    I1 = np.zeros(L, float)  # constant
    for i in range(0, L):
        I1[i] = 1
    x2 = np.convolve(y_values, I1, 'same')
    h = [1 / 33] * 33
    x3 = np.convolve(x2, h, 'same')
    return x3


# R2 - ekstrapolacja pierwszego rzędu
def first_order_extrapolation(y_values: [], L: int) -> []:
    I2 = np.zeros(2 * L, float)
    for i in range(0, L):
        I2[i] = (1 / L) * i
        I2[i + L] = 1 - (1 / L) * i
    result = np.convolve(y_values, I2, mode='same')
    h = [1 / 33] * 33
    result = np.convolve(result, h, mode='same')
    return result


# R3 - ekstrapolacja sinc
def sinc_extrapolation(y_values: [], L: int) -> []:
    N = len(y_values)
    I3 = np.zeros(N, float)
    for i in range(0, N):
        t = (N // 2 - i) / L
        if t == 0:
            v = 1
        else:
            v = np.sin(np.pi * t) / (np.pi * t)
        I3[i] = v

    result = np.convolve(y_values, I3, mode='same')
    h = [1 / 33] * 33
    result = np.convolve(result, h, mode='same')
    return result
