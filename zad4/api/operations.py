import cmath
import copy
import math

import numpy as np
from typing import List

from matplotlib import pyplot as plt


def add(y1: [], y2: []):
    return [y1[i] + y2[i] for i in range(len(y1))]


def sub(y1: [], y2: []):
    return [y1[i] - y2[i] for i in range(len(y1))]


def mul(y1: [], y2: []):
    return [y1[i] * y2[i] for i in range(len(y1))]


def div(y1: [], y2: []):
    return [y1[i] / y2[i] if y2[i] != 0 else 0 for i in range(len(y1))]


def convolution(y1: [], y2: []):
    x = y1
    h = y2
    n = len(x)
    m = len(h)
    y = np.zeros(n + m - 1, float)
    for i in range(0, n + m - 1):
        t = 0
        for j in range(0, n):
            if 0 <= i - j <= m - 1:
                t += x[j] * h[i - j]
        y[i] = t
    return y


def correlation_convolve(y1: [], y2: []) -> []:
    y2_reversed = y2[::-1]
    return convolution(y1, y2_reversed)


def correlation(y1: [], t1: [], y2: [], t2: []) -> []:
    len1 = len(y1)
    len2 = len(y2)
    y = []
    for i in range(len1 + len2 - 1):
        value = 0
        if i >= (len1 - 1):
            k1min = i - (len2 - 1)
        else:
            k1min = 0

        if i < (len1 - 1):
            k1max = i
        else:
            k1max = (len1 - 1)

        if i <= (len2 - 1):
            k2min = (len2 - 1 - i)
        else:
            k2min = 0

        k1 = k1min
        k2 = k2min
        while k1 <= k1max and k2 <= (len2 - 1):
            value += y1[k1] * y2[k2]
            k1 += 1
            k2 += 1
        y.append(value)

    t = np.linspace(t1[0], t1[-1] + t2[-1], len(y))
    return t, y


def next_lower_power_of_2(x):
    return 2**(x.bit_length() - 1)


def discrete_transformation_Fourier(y_values: []) -> []:
    N = len(y_values)
    N_padded = next_lower_power_of_2(N)
    y_values = y_values[:N_padded]
    N = len(y_values)

    result = []
    for m in range(N):
        sum = 0
        for n in range(N):
            sum += y_values[n] * cmath.exp(-2j * cmath.pi * m * n / N)
        result.append(sum)
    return result


def fast_discrete_fourier_transform(y_values: []) -> []:
    N = len(y_values)
    N_padded = next_lower_power_of_2(N)
    y_values = y_values[:N_padded]
    y_values = mix_samples(y_values)
    W = calculate_vector_of_w_params(len(y_values))

    N = 2
    while N <= len(y_values):
        for i in range(len(y_values) // N):
            for m in range(N // 2):
                offset = i * N
                tmp = y_values[offset + m + N // 2] * retrieve_w_from_vector(N, -m, W)
                y_values[offset + m + N // 2] = y_values[offset + m] - tmp
                y_values[offset + m] = y_values[offset + m] + tmp
        N *= 2

    return y_values


def retrieve_w_from_vector(N, k, vectorW):
    k = k % N
    if k < 0:
        k += N

    k = k * ((len(vectorW) * 2) // N)
    if k < len(vectorW):
        return vectorW[k]
    else:
        return vectorW[k - len(vectorW)] * -1


def calculate_vector_of_w_params(N):
    Warg = 2.0 * np.pi / N
    W = np.exp(-1j * Warg)
    allW = [W ** i for i in range(N // 2)]
    return allW


def reverse_bits(value, numberOfBits):
    reversed_value = 0
    for i in range(numberOfBits):
        if (value >> i) & 1:
            reversed_value |= 1 << (numberOfBits - 1 - i)
    return reversed_value


def mix_samples(samples):
    N = len(samples)
    numberOfBits = int(np.log2(N))
    mixed_samples = np.zeros(N, dtype=complex)
    for i in range(N):
        reversed_i = reverse_bits(i, numberOfBits)
        mixed_samples[reversed_i] = samples[i]
    return mixed_samples


def discrete_cosine_transform(y_values: []) -> []:
    N = len(y_values)
    N_padded = next_lower_power_of_2(N)
    y_values = y_values[:N_padded]
    N = len(y_values)
    result = []
    for m in range(N):
        sum = 0
        for n in range(N):
            sum += y_values[n] * math.cos(np.pi * (2.0 * n + 1) * m / (2.0 * N))
        if m == 0:
            sum *= math.sqrt(1.0 / N)
        else:
            sum *= math.sqrt(2.0 / N)
        result.append(sum)
    return result


def walsh_hadamard_transform(y_values: []) -> []:
    N = len(y_values)
    N_padded = next_lower_power_of_2(N)
    y_values = y_values[:N_padded]
    N = len(y_values)
    result = []
    for k in range(N):
        sum = 0
        for n in range(N):
            sum += y_values[n] * (-1) ** (bin(n & k).count('1'))
        result.append(sum)
    return result
