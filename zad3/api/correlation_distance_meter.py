import math

import numpy as np

from zad3.api.operations import correlation


class CorrelationDistanceMeter:
    def __init__(self,
                 transmitter_measurments_no: int, transmitter_time_unit: float,
                 transmitter_real_object_speed: float, transmitter_signal_speed_abstract: float,
                 receiver_signal_period, receiver_sampling_frequency,
                 receiver_buffers_length, receiver_report_period):

        self.transmitter_measurments_no = transmitter_measurments_no
        self.transmitter_time_unit = transmitter_time_unit
        self.transmitter_real_object_speed = transmitter_real_object_speed
        self.transmitter_signal_speed_abstract = transmitter_signal_speed_abstract
        self.receiver_signal_period = receiver_signal_period
        self.receiver_sampling_frequency = receiver_sampling_frequency
        self.receiver_buffers_length = receiver_buffers_length
        self.receiver_report_period = receiver_report_period

        self.t_values = []

        self.correlation_samples_y = None
        self.correlation_samples_t = None

        self.probing_signal_t = None
        self.probing_signal_y = None

        self.feedback_signal_t = None
        self.feedback_signal_signal_y = None

    def original_distances(self) -> []:
        result = []
        points = np.arange(0, self.transmitter_measurments_no * self.receiver_report_period,
                           self.receiver_report_period)
        for i in points:
            result.append(i * self.transmitter_real_object_speed)
        return result

    def receiver_distances(self):
        result = []
        amplitude = 1.0
        duration = self.receiver_buffers_length / self.receiver_sampling_frequency

        points = np.arange(0, self.transmitter_measurments_no * self.receiver_report_period,
                           self.receiver_report_period)
        self.t_values = []
        for i in points:
            self.t_values.append(i)
            distance = i * self.transmitter_real_object_speed
            propagation_time = 2 * distance / self.transmitter_signal_speed_abstract

            self.probing_signal_t, self.probing_signal_y = self.signal_values(amplitude, self.receiver_signal_period, i, duration, self.receiver_sampling_frequency)
            self.feedback_signal_t, self.feedback_signal_signal_y = self.signal_values(amplitude, self.receiver_signal_period, i - duration + propagation_time, duration, self.receiver_sampling_frequency)

            self.correlation_samples_t, self.correlation_samples_y = correlation(self.probing_signal_y, self.probing_signal_t, self.feedback_signal_signal_y, self.feedback_signal_t)
            result.append(self.receiver_get_distance(self.correlation_samples_y, self.receiver_sampling_frequency, self.transmitter_signal_speed_abstract))

        return result

    def receiver_get_distance(self, correlation_samples: [], frequency, signal_speed):
        midpoint = int(len(correlation_samples) / 2)
        right = correlation_samples[midpoint:]
        max_value = right.index(max(right))
        t_delay = max_value / frequency
        return round((t_delay * signal_speed) / 2, 3)

    def signal_values(self, amplitude, period, time_start, duration, sampling_frequency) -> tuple:
        y_values = []

        for t in np.arange(time_start, time_start + duration, 1 / sampling_frequency):
            y_values.append(sin_signal_distancemeter(amplitude, period, t))

        t_values = np.arange(time_start, time_start + duration, 1 / sampling_frequency)

        return t_values, y_values

    def calculate(self) -> tuple:
        original_values = self.original_distances()
        received_values = self.receiver_distances()
        diff = np.round(np.fabs(original_values - received_values), 3)
        return original_values, received_values, diff


def sin_signal_distancemeter(A: float, T: float, t: float):
    return A * math.sin((2 * math.pi / T) * t) + A * math.sin((2 * math.pi / T * 2) * t)
