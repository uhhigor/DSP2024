import math


def average_value(y_values):
    samples = len(y_values)
    n = 0
    sumxt = 0
    while n < samples:
        if math.isnan(y_values[n]):
            n += 1
            continue
        sumxt += y_values[n]
        n += 1

    return sumxt / samples


def average_value_absolute(y_values):
    samples = len(y_values)
    n = 0
    sumxt = 0
    while n < samples:
        if math.isnan(y_values[n]):
            n += 1
            continue
        sumxt += math.fabs(y_values[n])
        n += 1

    return sumxt / samples


def average_power(y_values):
    samples = len(y_values)
    n = 0
    sumxt = 0
    while n < samples:
        if math.isnan(y_values[n]):
            n += 1
            continue
        sumxt += y_values[n] ** 2
        n += 1

    return sumxt / samples


def continuous_variance(y_values):
    samples = len(y_values)
    n = 0
    sumxt = 0
    avg_value = average_value(y_values)
    while n < samples:
        if math.isnan(y_values[n]):
            n += 1
            continue
        sumxt += (y_values[n] - avg_value) ** 2
        n += 1

    return sumxt / samples


def continuous_effective_value(y_values):
    return math.sqrt(average_power(y_values))


def mean_square_error(y_values, y_values2):
    samples = len(y_values)
    n = 0
    sumxt = 0
    while n < samples:
        if math.isnan(y_values[n]) or math.isnan(y_values2[n]):
            n += 1
            continue
        sumxt += (y_values[n] - y_values2[n]) ** 2
        n += 1

    return sumxt / samples


def signal_to_noise_ratio(y_values, y_values2):
    mse = mean_square_error(y_values, y_values2)
    if mse == 0:
        return float('inf')
    return 10 * math.log10(average_power(y_values) / mse)


def maximum_difference(y_values, y_values2):
    samples = len(y_values)
    n = 0
    max_diff = 0
    while n < samples:
        if math.isnan(y_values[n]) or math.isnan(y_values2[n]):
            n += 1
            continue
        diff = math.fabs(y_values[n] - y_values2[n])
        if diff > max_diff:
            max_diff = diff
        n += 1

    return max_diff
