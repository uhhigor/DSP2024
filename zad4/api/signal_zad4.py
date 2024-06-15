import math

import numpy as np


def get_low_pass_filter(M: int, f0: float, fp: float, window: () = None) -> []:
    t_values = []
    y_values = []
    for n in range(M):
        t_values.append(n * (1.0 / fp))
        k = fp / f0
        c = (M - 1) / 2
        if n == c:
            res = 2.0 / k
        else:
            res = math.sin(2.0 * math.pi * (n - c) / k) / (math.pi * (n - c))

        if window is not None:
            res *= window(M, n)
        y_values.append(res)
    return t_values, y_values


def get_high_pass_filter(M: int, f0: float, fp: float, window: () = None) -> []:
    t_values, y_values = get_low_pass_filter(M, f0, fp, window)
    for i in range(len(y_values)):
        y_values[i] *= math.pow(-1, i)
    return t_values, y_values


def hamming_window(M: int, n: float) -> float:
    return 0.53836 - 0.46164 * math.cos(2.0 * math.pi * n / M)



