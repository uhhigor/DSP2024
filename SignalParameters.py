import math


def average_value(y_values):
    samples = len(y_values)
    n = 0
    sumxt = 0
    while n < samples:
        sumxt += y_values[n]
        n += 1

    return sumxt / samples


def average_value_absolute(y_values):
    samples = len(y_values)
    n = 0
    sumxt = 0
    while n < samples:
        sumxt += math.fabs(y_values[n])
        n += 1

    return sumxt / samples


def average_power(y_values):
    samples = len(y_values)
    n = 0
    sumxt = 0
    while n < samples:
        sumxt += y_values[n] ** 2
        n += 1

    return sumxt / samples


def continuous_variance(y_values):
    samples = len(y_values)
    n = 0
    sumxt = 0
    avg_value = average_value(y_values)
    while n < samples:
        sumxt += (y_values[n] - avg_value) ** 2
        n += 1

    return sumxt / samples


def continuous_effective_value(y_values):
    return math.sqrt(average_power(y_values))