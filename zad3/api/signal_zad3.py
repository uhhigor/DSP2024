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


def apply_low_pass_filter(y_values: np.ndarray, M: int, f_0: float, sample_rate: float, window_func=None) -> np.ndarray:
    # Calculate the cutoff frequency in radians per sample
    omega_c = 2 * np.pi * f_0 / sample_rate
    # Create an array for the filter coefficients
    h = np.zeros(M)
    # Calculate the filter coefficients (sinc function)
    for n in range(M):
        m = n - (M - 1) / 2
        if m == 0:
            h[n] = omega_c / np.pi
        else:
            h[n] = np.sin(omega_c * m) / (np.pi * m)

    if window_func is None:
        # rectangular window
        window = np.ones(M)
    else:
        # Apply the window function
        window = window_func(M)

    h *= window

    h /= np.sum(h)

    filtered_y = convolution(y_values, h)

    return filtered_y



def hamming_window(M: int) -> np.ndarray:
    window = np.zeros(M)
    for n in range(M):
        window[n] = 0.53836 - 0.46164 * np.cos(2 * np.pi * n / M)
    return window