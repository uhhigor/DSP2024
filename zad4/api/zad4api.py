import math
from math import sin, pi

import numpy as np


def s1(x):
    return 2 * sin(pi * x + pi / 2) + 5 * sin(4 * pi * x + pi / 2)


def s2(x):
    return 2 * sin(pi * x) + sin(2 * pi * x) + 5 * sin(4 * pi * x)


def s3(x):
    return 5 * sin(pi * x) + 5 * sin(8 * pi * x)


def get_values(func, t_values):
    return [func(t) for t in t_values]


def next_lower_power_of_2(x):
    return np.power(2, math.ceil(np.log2(x)))


def zero_padding(x):
    N = len(x)
    next_power = next_lower_power_of_2(N)
    new_x = np.zeros(next_power, dtype=complex)
    new_x[:N] = x
    return new_x


def dit_fft(x: []):
    x = zero_padding(x)
    N = len(x)
    stage_num = int(np.log2(N))
    x = bit_reverse_copy(x)

    for s in range(1, stage_num + 1):
        p = np.power(2, s)
        half = p // 2
        W_p = np.exp(-2j * np.pi / p)

        for i in range(0, N, p):
            W = 1
            for j in range(half):
                t = W * x[i + j + half]

                x[i + j + half] = x[i + j] - t
                x[i + j] = x[i + j] + t

                W *= W_p

    result = (x * 2) / N
    return result


def dif_fft(x: []):
    x = zero_padding(x)
    N = len(x)
    stage_num = int(np.log2(N))
    x = bit_reverse_copy(x)

    for s in range(1, stage_num + 1):
        p = np.power(2, s)
        half = p // 2
        W_p = np.exp(-2j * np.pi / p)

        for i in range(0, N, p):
            W = 1
            for j in range(half):
                t = W * x[i + j + half]
                u = x[i + j]
                x[i + j] = u + t
                x[i + j + half] = u - t
                W *= W_p
    result = (x * 2) / N
    return result


def dct_ii(ys: []) -> []:
    N = len(ys) # length of the signal
    transform = [complex(y) for y in ys] # Convert the signal to complex numbers
    X = [0] * N # empty list of the same length as the signal

    for m in range(N):
        sum = 0
        for n in range(N):
            sum += (transform[n]
                    * math.cos((math.pi * (2*n + 1) * m) / (2*N)))
        if m == 0:
            X[m] = math.sqrt(1 / N)
        else:
            X[m] = math.sqrt(2 / N) * sum
    return X


def hadamard_matrix(n):
    if n == 1:
        return [1]
    else:
        H_n = hadamard_matrix(n // 2)
        top = np.concatenate((H_n, H_n), axis=1)
        bottom = np.concatenate((H_n, -H_n), axis=1)
        H_2n = np.concatenate((top, bottom), axis=0)
        return H_2n


def walsh_hadamard_transform(x):
    N = len(x)
    n = next_lower_power_of_2(N)
    padded_x = zero_padding(x)
    H = hadamard_matrix(n)
    transformed_x = np.dot(H, padded_x)
    return transformed_x[:N]


def bit_reverse_copy(x):
    N = len(x)
    j = 0
    y = np.zeros(N, dtype=complex)
    for i in range(N):
        y[j] = x[i]
        m = N // 2
        while m >= 1 and j >= m:
            j -= m
            m //= 2
        j += m
    return y
