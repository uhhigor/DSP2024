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
def conversion_sampling(signal: DigitalSignal, number_of_samples):
    N = len(signal.samples)
    M = number_of_samples
    L = N // M
    print(M)
    x1 = np.zeros(N, float)
    for i in range(0, M):
        print(int(i * L))
        print(signal.samples[int(i * L)])
        x1[int(i * L)] = signal.samples[int(i * L)]
    return DigitalSignal(start_time=signal.start_time, sampling_rate=signal.sampling_rate, samples=x1, time=signal.time), L

# Q2 - kwantyzacja równomierna z zaokrągleniem
def uniform_quantization(signal: DigitalSignal) -> DigitalSignal:
    samples = [np.round(sample) for sample in signal.samples]
    return DigitalSignal(start_time=signal.start_time, sampling_rate=signal.sampling_rate, samples=samples, time=signal.time)


# R1 - ekstrapolacja zerowego rzędu

def zero_order_extrapolation(signal: DigitalSignal, L) -> DigitalSignal:
    I1 = np.zeros(L, float)
    for i in range(0, L):
        I1[i] = 1

    x2 = np.convolve(signal.samples, I1, 'same')
    h = [1 / 33] * 33
    #x3 = np.convolve(x2, h, 'same')

    return DigitalSignal(start_time=signal.start_time, sampling_rate=signal.sampling_rate, samples=x2, time=signal.time)


# R2 - ekstrapolacja pierwszego rzędu
def first_order_extrapolation(signal: DigitalSignal) -> DigitalSignal:
    I2 = np.zeros(2 * len(signal.samples), float)
    for i in range(len(signal.samples)):
        I2[i] = (1 / len(signal.samples)) * i
        I2[i + len(signal.samples)] = 1 - (1 / len(signal.samples)) * i
    result = np.convolve(signal.samples, I2, mode='same')
    h = [1 / 33] * 33
    result = np.convolve(result, h, mode='same')
    signal.samples = result
    return signal


# R3 - ekstrapolacja sinc
def sinc_extrapolation(signal: DigitalSignal) -> DigitalSignal:
    I3 = np.zeros(len(signal.samples), float)
    for i in range(len(signal.samples)):
        t = (len(signal.samples) // 2 - i) / len(signal.samples)
        if t == 0:
            v = 1
        else:
            v = np.sin(np.pi * t) / (np.pi * t)
        I3[i] = v

    result = np.convolve(signal.samples, I3, mode='same')
    h = [1 / 33] * 33
    result = np.convolve(result, h, mode='same')
    signal.samples = result
    return signal
