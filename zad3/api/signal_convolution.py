import numpy as np


def convolution(y1, y2):
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

def convolution2(y1, y2):
    return np.convolve(y1, y2, 'same')
