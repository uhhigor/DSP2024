import math

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from zad3.api.operations import correlation


class CorrelationDistanceMeter:
    def __init__(self,
                 transmitter_measurments_no: int,
                 transmitter_real_object_speed: float, transmitter_signal_speed_abstract: float,
                 receiver_signal_period, receiver_sampling_frequency,
                 receiver_buffers_length, receiver_report_period, fixed_time: bool):

        self.transmitter_measurments_no = transmitter_measurments_no
        self.transmitter_real_object_speed = transmitter_real_object_speed
        self.transmitter_signal_speed_abstract = transmitter_signal_speed_abstract
        self.receiver_signal_period = receiver_signal_period
        self.receiver_sampling_frequency = receiver_sampling_frequency
        self.receiver_buffers_length = receiver_buffers_length
        self.receiver_report_period = receiver_report_period

        self.fixed_time = fixed_time

        self.t_values_probing = []
        self.t_values_feedback = []

        self.correlation_samples_y = None

        self.probing_signal_y = None

        self.feedback_signal_y = None

        self.fig = None

        self.y_values_probing_all = []
        self.t_values_probing_all = []
        self.y_values_feedback_all = []
        self.t_values_feedback_all = []
        self.correlation_samples_y_all = []
        self.anim = None
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1)
        self.fig.show()

    def original_distance(self) -> []:
        result = []
        points = np.arange(0, self.transmitter_measurments_no * self.receiver_report_period,
                           self.receiver_report_period)
        for i in points:
            result.append(i * self.transmitter_real_object_speed)
        return result

    def receiver_distances(self):
        distances = []
        shifts = []
        amplitude = 2.0
        duration = self.receiver_buffers_length / self.receiver_sampling_frequency
        points = np.arange(0, self.transmitter_measurments_no * self.receiver_report_period,
                           self.receiver_report_period)
        self.t_values = []
        for i in points:
            self.t_values.append(i)
            curr_distance = i * self.transmitter_real_object_speed
            propagation_time = 2 * curr_distance / self.transmitter_signal_speed_abstract
            self.probing_signal_y, self.t_values_probing = self.signal_values(amplitude, self.receiver_signal_period,
                                                                              i - duration, duration,
                                                                              self.receiver_sampling_frequency)
            self.feedback_signal_y, self.t_values_feedback = self.signal_values(amplitude, self.receiver_signal_period,
                                                                                i - duration + propagation_time,
                                                                                duration,
                                                                                self.receiver_sampling_frequency)

            self.correlation_samples_y = correlation(self.probing_signal_y, self.feedback_signal_y)

            distance, shift = self.calculate_distance(self.correlation_samples_y, self.receiver_sampling_frequency,
                                                      self.transmitter_signal_speed_abstract)

            self.t_values_probing_all.append(self.t_values_probing)
            self.y_values_probing_all.append(self.probing_signal_y)
            self.y_values_feedback_all.append(self.feedback_signal_y)
            self.t_values_feedback_all.append(self.t_values_feedback)
            self.correlation_samples_y_all.append(self.correlation_samples_y)

            distances.append(distance)
            shifts.append(shift)

        return distances, points, shifts

    def get_receiver_t_values(self):
        return self.t_values

    def calculate_distance(self, correlation_samples: [], frequency, signal_speed):
        right_half = correlation_samples[len(correlation_samples) // 2:]
        max_value = max(right_half)
        max_index = right_half.index(max_value)
        shift = max_index / frequency
        return (shift * signal_speed) / 2, shift

    def signal_values(self, amplitude, period, time_start, duration, sampling_frequency) -> []:
        y_values = []
        t_values = []

        for t in np.arange(time_start, time_start + duration, 1 / sampling_frequency):
            y_values.append(sin_signal_distancemeter(amplitude, period, t))
            t_values.append(t)

        return y_values, t_values

    def calculate_avg_speed(self, received_values, t) -> float:
        sum_distance = 0
        for i in received_values:
            sum_distance += i

        sum_t = 0
        for i in t:
            sum_t += i

        return sum_distance / sum_t


    def calculate(self) -> tuple:
        original_values = self.original_distance()
        received_values, t, shifts = self.receiver_distances()

        diff = np.round(np.fabs(np.array(original_values) - np.array(received_values)), 3)

        avg_speed = self.calculate_avg_speed(received_values, t)
        self.show_plot()
        return original_values, received_values, t, diff, shifts, avg_speed

    def update_plot(self, i, l1, l2, l3):
        if self.fixed_time:
            t_prob = np.linspace(self.t_values_probing_all[i][0], self.t_values_probing_all[i][-1], len(self.y_values_probing_all[i]))
            t_feed = np.linspace(self.t_values_probing_all[i][0], self.t_values_probing_all[i][-1], len(self.y_values_feedback_all[i]))
            l1.set_data(t_feed, self.y_values_probing_all[i])
            l2.set_data(t_prob, self.y_values_feedback_all[i])
        else:
            l1.set_data(self.t_values_probing_all[i], self.y_values_probing_all[i])
            l2.set_data(self.t_values_feedback_all[i], self.y_values_feedback_all[i])

        corr_len = len(self.correlation_samples_y_all[i])
        x = np.linspace(-(corr_len // 2), (corr_len // 2), corr_len)
        l3.set_data(x, self.correlation_samples_y_all[i])

    def show_plot(self):
        t_0 = self.t_values_probing_all[0][0]
        t_1 = self.t_values_probing_all[0][-1]
        t_prob = np.arange(t_0, t_1, (t_1 - t_0) / len(self.y_values_probing_all[0]))
        t_feed = np.arange(t_0, t_1, (t_1 - t_0) / len(self.y_values_feedback_all[0]))

        t_start = 0
        t_end = self.transmitter_measurments_no * self.receiver_report_period
        self.ax1.set_xlim(t_start, t_end)
        self.ax2.set_xlim(t_start, t_end)
        self.ax1.set_title("Sygnał sondujący")
        self.ax1.set_xlabel("Czas [s]")
        self.ax1.set_ylabel("Amplituda")
        l1,  = self.ax1.plot(t_prob, self.y_values_probing_all[0])

        self.ax2.set_title("Sygnał odbity")
        self.ax2.set_xlabel("Czas [s]")
        self.ax2.set_ylabel("Amplituda")
        l2,  = self.ax2.plot(t_feed, self.y_values_feedback_all[0])

        self.ax3.set_title("Korelacja sygnałów")
        self.ax3.set_ylabel("Amplituda")
        x = np.arange(-len(self.correlation_samples_y_all[0]) // 2, len(self.correlation_samples_y_all[0]) // 2)
        l3,  = self.ax3.plot(x, self.correlation_samples_y_all[0])

        plt.subplots_adjust(hspace=1)

        if self.anim is None:
            self.anim = FuncAnimation(self.fig, self.update_plot, frames=self.transmitter_measurments_no,
                                fargs=(l1, l2, l3), repeat=True, interval=1000)

    def __del__(self):
        plt.close(self.fig)

def sin_signal_distancemeter(A: float, T: float, t: float):
    return A * math.sin(2.0 * math.pi * t / T)
