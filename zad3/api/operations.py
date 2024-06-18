import numpy as np


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
    return np.convolve(y1, y2_reversed)


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
    return y, t
