# GUI setup
import math
import time
from tkinter import Tk, ttk

from matplotlib import pyplot as plt

from zad4.api import zad4api as api

import numpy as np

root = Tk()
root.title("CPS - Zadanie 4 | Transformacje")
main_frame = ttk.Frame(root, padding="10")


def show_current_signal():
    y_values = get_signal_values()
    t_values = np.linspace(0, 10, len(y_values))
    fig, ax = plt.subplots()
    ax.scatter(t_values, y_values)
    ax.plot(t_values, y_values)
    plt.show()


def get_signal_values():
    selected_signal = signal_dropdown.get()
    N = int(math.pow(2, int(n_entry.get())))
    t_values = np.arange(0, 10, 1 / N)
    if selected_signal == "s1":
        return api.get_values(api.s1, t_values)
    elif selected_signal == "s2":
        return api.get_values(api.s2, t_values)
    elif selected_signal == "s3":
        return api.get_values(api.s3, t_values)


def get_frequency_values(t_values):
    N = len(t_values)  # Number of sample points
    T = t_values[1] - t_values[0]  # Sample spacing
    xf = np.fft.fftfreq(N, T)
    return np.fft.fftshift(xf)  # Shift the zero frequency component to the center


# DFT Button
def execute_dit_fft():
    y_values = get_signal_values()
    N = int(math.pow(2, int(n_entry.get())))
    start_time = time.perf_counter()
    result = api.dit_fft(y_values)
    end_time = time.perf_counter()
    result_time = end_time - start_time

    real_parts = [val.real for val in result]
    imag_parts = [val.imag for val in result]

    t_values = np.linspace(0, N, len(real_parts))

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
    fig.suptitle("DIT FFT - " + signal_dropdown.get() + " signal")
    plt.subplots_adjust(hspace=1)

    ax1.scatter(t_values, real_parts, s=10, color="red")
    ax1.plot(t_values, real_parts)
    ax1.set_title("Real")
    ax1.set_xlabel("Frequency")

    ax2.scatter(t_values, imag_parts, s=10, color="red")
    ax2.plot(t_values, imag_parts)
    ax2.set_title("Imaginary")
    ax2.set_xlabel("Frequency")

    magnitudes = np.abs(result)
    ax3.scatter(t_values, magnitudes, s=10, color="red")
    ax3.plot(t_values, magnitudes)
    ax3.set_title("Magnitude")
    ax3.set_xlabel("Frequency")

    phases = np.angle(result)
    ax4.scatter(t_values, phases, s=10, color="red")
    ax4.plot(t_values, phases)
    ax4.set_title("Phase")
    ax4.set_xlabel("Frequency")

    fig.text(0.5, 0.01, "Time: " + str(round(result_time, 6)), ha='center')
    plt.show()


ttk.Button(main_frame, text="DIT FFT", command=lambda: execute_dit_fft()).pack()


def execute_dif_fft():
    y_values = get_signal_values()
    N = int(math.pow(2, int(n_entry.get())))

    start_time = time.perf_counter()
    result = api.dif_fft(y_values)
    end_time = time.perf_counter()
    result_time = end_time - start_time

    real_parts = [val.real for val in result]
    imag_parts = [val.imag for val in result]

    t_values = np.linspace(0, N, len(real_parts))

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
    fig.suptitle("DIF FFT - " + signal_dropdown.get() + " signal")
    plt.subplots_adjust(hspace=1)

    ax1.scatter(t_values, real_parts, s=10, color="red")
    ax1.plot(t_values, real_parts)
    ax1.set_title("Real")
    ax1.set_xlabel("Frequency")

    ax2.scatter(t_values, imag_parts, s=10, color="red")
    ax2.plot(t_values, imag_parts)
    ax2.set_title("Imaginary")
    ax2.set_xlabel("Frequency")

    magnitudes = np.abs(result)
    ax3.scatter(t_values, magnitudes, s=10, color="red")
    ax3.plot(t_values, magnitudes)
    ax3.set_title("Magnitude")
    ax3.set_xlabel("Frequency")

    phases = np.angle(result)
    ax4.scatter(t_values, phases, s=10, color="red")
    ax4.plot(t_values, phases)
    ax4.set_title("Phase")
    ax4.set_xlabel("Frequency")

    fig.text(0.5, 0.01, "Time: " + str(round(result_time, 6)), ha='center')
    plt.show()


ttk.Button(main_frame, text="DIF FFT", command=lambda: execute_dif_fft()).pack()


def execute_dct_ii():
    y_values = get_signal_values()
    N = int(math.pow(2, int(n_entry.get())))

    start_time = time.perf_counter()
    result = api.dct_ii(y_values)
    end_time = time.perf_counter()
    result_time = end_time - start_time

    real_parts = [val.real for val in result]
    imag_parts = [val.imag for val in result]

    t_values = np.linspace(0, N, len(real_parts))

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
    fig.suptitle("DCT II - " + signal_dropdown.get() + " signal")
    plt.subplots_adjust(hspace=1)

    ax1.scatter(t_values, real_parts, s=10, color="red")
    ax1.plot(t_values, real_parts)
    ax1.set_title("Real")
    ax1.set_xlabel("Frequency")

    ax2.scatter(t_values, imag_parts, s=10, color="red")
    ax2.plot(t_values, imag_parts)
    ax2.set_title("Imaginary")
    ax2.set_xlabel("Frequency")

    magnitudes = np.abs(result)
    ax3.scatter(t_values, magnitudes, s=10, color="red")
    ax3.plot(t_values, magnitudes)
    ax3.set_title("Magnitude")
    ax3.set_xlabel("Frequency")

    phases = np.angle(result)
    ax4.scatter(t_values, phases, s=10, color="red")
    ax4.plot(t_values, phases)
    ax4.set_title("Phase")
    ax4.set_xlabel("Frequency")

    fig.text(0.5, 0.01, "Time: " + str(round(result_time, 6)), ha='center')
    plt.show()


ttk.Button(main_frame, text="DCT II", command=lambda: execute_dct_ii()).pack()


def execute_walsh_had():
    y_values = get_signal_values()
    N = int(math.pow(2, int(n_entry.get())))

    start_time = time.perf_counter()
    result = api.walsh_hadamard_transform(y_values)
    end_time = time.perf_counter()
    result_time = end_time - start_time

    real_parts = [val.real for val in result]
    imag_parts = [val.imag for val in result]

    t_values = np.linspace(0, N, len(real_parts))

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
    fig.suptitle("WALSH-HADAMARD - " + signal_dropdown.get() + " signal")
    plt.subplots_adjust(hspace=1)

    ax1.scatter(t_values, real_parts, s=10, color="red")
    ax1.plot(t_values, real_parts)
    ax1.set_title("Real")
    ax1.set_xlabel("Frequency")

    ax2.scatter(t_values, imag_parts, s=10, color="red")
    ax2.plot(t_values, imag_parts)
    ax2.set_title("Imaginary")
    ax2.set_xlabel("Frequency")

    magnitudes = np.abs(result)
    ax3.scatter(t_values, magnitudes, s=10, color="red")
    ax3.plot(t_values, magnitudes)
    ax3.set_title("Magnitude")
    ax3.set_xlabel("Frequency")

    phases = np.angle(result)
    ax4.scatter(t_values, phases, s=10, color="red")
    ax4.plot(t_values, phases)
    ax4.set_title("Phase")
    ax4.set_xlabel("Frequency")

    fig.text(0.5, 0.01, "Time: " + str(round(result_time, 6)), ha='center')
    plt.show()


ttk.Button(main_frame, text="Walsh-Hadamard", command=lambda: execute_walsh_had()).pack()

ttk.Button(main_frame, text="Show current signal", command=lambda: show_current_signal()).pack()

# n label
ttk.Label(main_frame, text="n:").pack()
# n entry
n_entry = ttk.Entry(main_frame)
n_entry.insert(0, "4")
n_entry.pack()

# signal dropdown
signal_dropdown = ttk.Combobox(main_frame)
signal_dropdown['values'] = ("s1", "s2", "s3")
signal_dropdown.current(0)
signal_dropdown.pack()

########################################

main_frame.pack()
root.mainloop()
