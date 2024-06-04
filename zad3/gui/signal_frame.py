from tkinter import ttk, StringVar, Tk, font

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from zad3.api import analog_signal, signal_conversion, signal_zad3

signal_map = {
    "Szum o rozkładzie jednostajnym": analog_signal.S1,
    "Szum gaussowski": analog_signal.S2,
    "Sygnał sinusoidalny": analog_signal.S3,
    "Sygnał sinusoidalny wyprostowany jednopołówkowo": analog_signal.S4,
    "Sygnał sinusoidalny wyprostowany dwupołówkowo": analog_signal.S5,
    "Sygnał prostokątny": analog_signal.S6,
    "Sygnał prostokątny symetryczny": analog_signal.S7,
    "Sygnał trójkątny": analog_signal.S8,
    "Skok jednostkowy": analog_signal.S9
}


class SignalGenerator:
    def __init__(self, master):

        self.y_values = []
        self.t_values = []

        self.frame = ttk.Frame(master, padding="10")

        # Signal dropdown
        ttk.Label(self.frame, text="Sygnał: ").grid(column=0, row=0)
        self.signal_var = StringVar()
        self.signal_dropdown = ttk.OptionMenu(self.frame, self.signal_var, "Sygnał sinusoidalny",
                                              *list(signal_map.keys()))
        self.signal_dropdown.grid(column=1, row=0)

        # Amplitude
        ttk.Label(self.frame, text="Amplituda: ").grid(column=0, row=1)
        self.amplitude_entry = ttk.Entry(self.frame)
        self.amplitude_entry.insert(0, "1")
        self.amplitude_entry.grid(column=1, row=1)

        # Start time
        ttk.Label(self.frame, text="Czas początkowy: ").grid(column=0, row=2)
        self.start_time_entry = ttk.Entry(self.frame)
        self.start_time_entry.insert(0, "0")
        self.start_time_entry.grid(column=1, row=2)

        # Duration
        ttk.Label(self.frame, text="Czas trwania: ").grid(column=0, row=3)
        self.duration_entry = ttk.Entry(self.frame)
        self.duration_entry.insert(0, "1")
        self.duration_entry.grid(column=1, row=3)

        # Period
        ttk.Label(self.frame, text="Okres podstawowy: ").grid(column=0, row=4)
        self.period_entry = ttk.Entry(self.frame)
        self.period_entry.insert(0, "0.1")
        self.period_entry.grid(column=1, row=4)

        # kw

        ttk.Label(self.frame, text="Współczynnik wypełnienia: ").grid(column=0, row=5)
        self.kw_entry = ttk.Entry(self.frame)
        self.kw_entry.grid(column=1, row=5)
        self.kw_entry.config(state="disabled")

        def update_kw_entry(*args):
            if self.signal_var.get() == "Sygnał prostokątny symetryczny" or self.signal_var.get() == "Sygnał trójkątny" or self.signal_var.get() == "Sygnał prostokątny":
                self.kw_entry.config(state="normal")
            else:
                self.kw_entry.config(state="disabled")

        self.signal_var.trace("w", update_kw_entry)

        # ts
        ttk.Label(self.frame, text="Czas skoku: ").grid(column=0, row=6)
        self.ts_entry = ttk.Entry(self.frame)
        self.ts_entry.grid(column=1, row=6)
        self.ts_entry.config(state="disabled")

        def update_ts_entry(*args):
            if self.signal_var.get() == "Skok jednostkowy":
                self.ts_entry.config(state="normal")
            else:
                self.ts_entry.config(state="disabled")

        self.signal_var.trace("w", update_ts_entry)

        # Generate button
        ttk.Button(self.frame, text="Generuj sygnał analogowy", command=lambda: self.generate_analog_signal()).grid(
            column=0, row=7, columnspan=2)

        fig, self.ax = plt.subplots()
        self.ax.figure.set_size_inches(2, 1.5)
        self.ax.tick_params(axis='both', labelsize=3)
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=8, columnspan=2)

        # Signal conversion
        bold_font = font.Font(weight='bold')  # Create bold font
        ttk.Label(self.frame, text="Konwersja sygnału: ", font=bold_font).grid(column=0, row=9, columnspan=2)

        # Sampling
        self.sampling_frequency_entry = ttk.Entry(self.frame)
        self.sampling_frequency_entry.insert(0, "100")
        self.sampling_frequency_entry.grid(column=0, row=10)
        ttk.Button(self.frame, text="Wykonaj próbkowanie", command=lambda: self.execute_sampling()).grid(column=1,
                                                                                                         row=10,
                                                                                                         columnspan=2)

        # Quantization
        ttk.Button(self.frame, text="Wykonaj kwantyzację", command=lambda: self.execute_quantization()).grid(column=1,
                                                                                                             row=12,
                                                                                                             columnspan=2)

        # Reconstruction
        self.reconstruction_var = StringVar()
        self.reconstruction_dropdown = ttk.OptionMenu(self.frame, self.reconstruction_var,
                                                      "Interpolacja zerowego rzędu", "Interpolacja zerowego rzędu",
                                                      "Interpolacja pierwszego rzędu",
                                                      "Rekonstrukcja w oparciu o funkcje sinc")
        self.reconstruction_dropdown.grid(column=0, row=13)
        ttk.Button(self.frame, text="Wykonaj rekonstrukcję", command=lambda: self.execute_reconstruction()).grid(
            column=1, row=13)

    def generate_analog_signal(self):
        signal = signal_map[self.signal_var.get()]
        amplitude = float(self.amplitude_entry.get())
        start_time = float(self.start_time_entry.get())
        duration = float(self.duration_entry.get())
        period = float(self.period_entry.get())
        frequency = float(1.0 / period)

        if self.signal_var.get() == "Skok jednostkowy":
            ts = float(self.ts_entry.get())
            s = signal(amplitude, start_time, duration, period, ts)
        elif (self.signal_var.get() == "Sygnał prostokątny symetryczny"
              or self.signal_var.get() == "Sygnał trójkątny"
              or self.signal_var.get() == "Sygnał prostokątny"):
            kw = float(self.kw_entry.get())
            s = signal(amplitude, start_time, duration, period, kw)
        else:
            s = signal(amplitude, start_time, duration, period)
        self.t_values, self.y_values = s.get_simulated_values(start_time, start_time + duration)
        self.show_plot(self.signal_var.get() + " " + str(frequency) + "Hz", "plot")

    def show_plot(self, title: str, plot_type: str, clear: bool = True):
        if clear:
            self.ax.clear()
            self.canvas.draw()
        self.ax.set_title(title, fontsize=6)
        if plot_type == "plot":
            self.ax.plot(self.t_values, self.y_values, linewidth=0.5)
        elif plot_type == "scatter":
            self.ax.scatter(self.t_values, self.y_values, s=0.2)
        elif plot_type == "scatterplot":
            self.ax.scatter(self.t_values, self.y_values, s=0.2)
            self.ax.plot(self.t_values, self.y_values, linewidth=0.5)

        self.canvas.draw()

    def execute_sampling(self):
        num_samples = int(float(self.duration_entry.get()) * int(self.sampling_frequency_entry.get()))
        self.y_values = signal_conversion.uniform_sampling(self.y_values, num_samples)
        self.show_plot(self.signal_var.get(), "scatterplot")

    def execute_quantization(self):
        self.y_values = signal_conversion.uniform_quantization(self.y_values)
        self.show_plot(self.signal_var.get(), "scatterplot")

    def execute_reconstruction(self):
        num_samples = int(float(self.duration_entry.get()) * int(self.sampling_frequency_entry.get()))
        self.show_plot(self.signal_var.get(), "scatter", True)
        if self.reconstruction_var.get() == "Interpolacja zerowego rzędu":
            self.y_values = signal_conversion.zero_order_extrapolation(self.y_values,
                                                                       num_samples)
        elif self.reconstruction_var.get() == "Interpolacja pierwszego rzędu":
            self.y_values = signal_conversion.first_order_extrapolation(self.y_values,
                                                                        num_samples)
        elif self.reconstruction_var.get() == "Rekonstrukcja w oparciu o funkcje sinc":
            self.y_values = signal_conversion.sinc_extrapolation(self.y_values,
                                                                 num_samples)
        self.show_plot(self.signal_var.get(), "plot", False)
