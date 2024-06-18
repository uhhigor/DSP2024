import math

import numpy as np
from matplotlib import pyplot as plt

from zad3.api.operations import correlation


class CorrelationDistanceMeter:
    def __init__(self,
                 transmitter_measurments_no: int,
                 transmitter_real_object_speed: float, transmitter_signal_speed_abstract: float,
                 receiver_signal_period, receiver_sampling_frequency,
                 receiver_buffers_length, receiver_report_period):

        self.transmitter_measurments_no = transmitter_measurments_no
        self.transmitter_real_object_speed = transmitter_real_object_speed
        self.transmitter_signal_speed_abstract = transmitter_signal_speed_abstract
        self.receiver_signal_period = receiver_signal_period
        self.receiver_sampling_frequency = receiver_sampling_frequency
        self.receiver_buffers_length = receiver_buffers_length
        self.receiver_report_period = receiver_report_period

        self.t_values = []

        self.correlation_samples_y = None

        self.probing_signal_y = None

        self.feedback_signal_y = None

        self.fig = None

    def original_distance(self) -> []:
        result = []
        points = np.arange(0, self.transmitter_measurments_no * self.receiver_report_period,
                           self.receiver_report_period)
        for i in points:
            result.append(i * self.transmitter_real_object_speed)
        return result

    def receiver_distances(self):
        result = []
        amplitude = 2.0
        duration = self.receiver_buffers_length / self.receiver_sampling_frequency

        points = np.arange(0, self.transmitter_measurments_no * self.receiver_report_period, self.receiver_report_period)
        self.t_values = []
        for i in points:
            self.t_values.append(i)
            curr_distance = i * self.transmitter_real_object_speed
            propagation_time = 2 * curr_distance / self.transmitter_signal_speed_abstract

            self.probing_signal_y, self.t_values = self.signal_values(amplitude, self.receiver_signal_period,
                                                       i - duration, duration,
                                                       self.receiver_sampling_frequency)
            self.feedback_signal_y, t = self.signal_values(amplitude, self.receiver_signal_period,
                                                        i - duration + propagation_time,
                                                        duration,
                                                        self.receiver_sampling_frequency)

            self.correlation_samples_y, t = correlation(self.probing_signal_y, self.t_values, self.feedback_signal_y,
                                                     self.t_values)

            result.append(self.calculate_distance(self.correlation_samples_y, self.receiver_sampling_frequency,
                                                     self.transmitter_signal_speed_abstract))

        return result, points

    def get_receiver_t_values(self):
        return self.t_values

    def calculate_distance(self, correlation_samples: [], frequency, signal_speed):
        right_half = correlation_samples[len(correlation_samples) // 2:]
        max_value = max(right_half)
        max_index = right_half.index(max_value)
        t_delay = max_index / frequency
        return signal_speed * t_delay / 2

    def signal_values(self, amplitude, period, time_start, duration, sampling_frequency) -> []:
        y_values = []
        t_values = []

        for t in np.arange(time_start, time_start + duration, 1 / sampling_frequency):
            y_values.append(sin_signal_distancemeter(amplitude, period, t))
            t_values.append(t)

        return y_values, t_values

    def calculate(self) -> tuple:
        original_values = self.original_distance()
        received_values, t = self.receiver_distances()
        diff = np.round(np.fabs(np.array(original_values) - np.array(received_values)), 3)
        return original_values, received_values, t, diff

    def show_plot(self):
        plt.close(self.fig)
        self.fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

        ax1.set_title("Sygnał sondujący")
        ax1.set_xlabel("Czas [s]")
        ax1.set_ylabel("Amplituda")
        ax1.plot(self.t_values, self.probing_signal_y)

        ax2.set_title("Sygnał odbity")
        ax2.set_xlabel("Czas [s]")
        ax2.set_ylabel("Amplituda")
        ax2.plot(self.t_values, self.feedback_signal_y)

        ax3.set_title("Korelacja sygnałów")
        ax3.set_ylabel("Amplituda")
        x = np.arange(-len(self.correlation_samples_y) // 2, len(self.correlation_samples_y) // 2)
        ax3.plot(x, self.correlation_samples_y)

        plt.subplots_adjust(hspace=1)
        self.fig.show()


def sin_signal_distancemeter(A: float, T: float, t: float):
    return A * math.sin(2.0 * math.pi * t / T)
