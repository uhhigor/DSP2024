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
