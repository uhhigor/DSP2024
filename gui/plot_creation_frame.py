from tkinter import ttk, StringVar, Toplevel

import numpy as np
from matplotlib import pyplot as plt

from api import analog_signal, signal_conversion, digital_signal
from signal_info_frame import SignalInfoFrame

signal_map = {
    "None": None,
    "Szum o rozkładzie jednostajnym": analog_signal.S1,
    "Szum gaussowski": analog_signal.S2,
    "Sygnał sinusoidalny": analog_signal.S3,
    "Sygnał sinusoidalny wyprostowany jednopołówkowo": analog_signal.S4,
    "Sygnał sinusoidalny wyprostowany dwupołówkowo": analog_signal.S5,
    "Sygnał prostokątny": analog_signal.S6,
    "Sygnał prostokątny symetryczny": analog_signal.S7,
    "Sygnał trójkątny": analog_signal.S8,
    "Skok jednostkowy": analog_signal.S9,
    "Impuls jednostkowy": analog_signal.S10,
    "Szum impulsowy": analog_signal.S11
}
signals = list(signal_map.keys())


def only_numbers(char: chr):
    return char.isdigit() or char == "."


class PlotCreationFrame:
    def __init__(self, master, title):
        self.windows = []
        self.master = master
        self.frame = ttk.Frame(self.master, padding="10")
        self.params_frame = ttk.Frame(self.frame)
        self.params_frame.grid(column=0, row=2, columnspan=2, rowspan=6)
        self.current = None
        self.current_analog = None
        self.title = title

        # Choose signal
        self.init_choose_signal()

        # Signal parameters
        self.init_signal_parameters()

        self.selected_signal.trace("w", self.show_params)

        ttk.Label(self.frame, text=title, font=("Helvetica", 32)).grid(column=0, row=0)
        # Generate button
        ttk.Button(self.frame, text="Generate", command=self.generate_btn).grid(column=0, row=8)

        # Save to file button
        ttk.Button(self.frame, text="Save to file",
                   command=lambda: self.save_to_file(self.current['signal'], self.current['samples'],
                                                     self.current['y_values'],
                                                     self.file_name_entry.get() + '.bin')).grid(column=2, row=4)

        # Load from file button
        ttk.Button(self.frame, text="Load from file", command=self.load_from_file).grid(
            column=2, row=5)
        ttk.Label(self.frame, text="Nazwa pliku: ").grid(column=2, row=6)
        self.file_name_entry = ttk.Entry(self.frame)
        self.file_name_entry.grid(column=3, row=6)
        self.file_name_entry.insert(0, "signal")
        # Show params
        self.show_params()

    def init_choose_signal(self):
        ttk.Label(self.frame, text="Wybierz sygnał:").grid(column=0, row=1)
        self.selected_signal = StringVar()
        dropdown_signal = ttk.OptionMenu(self.frame, self.selected_signal, *signals)
        dropdown_signal.config(width=30)
        dropdown_signal.grid(column=1, row=1)
        self.selected_signal.set("Szum o rozkładzie jednostajnym")

    def init_signal_parameters(self):
        self.f_label = ttk.Label(self.params_frame, text="Częstotliwość próbkowania f: ")
        self.f_entry = ttk.Entry(self.params_frame, validate="key",
                                 validatecommand=(self.master.register(only_numbers), "%S"))

        self.A_label = ttk.Label(self.params_frame, text="Amplituda sygnału A: ")
        self.A_entry = ttk.Entry(self.params_frame, validate="key",
                                 validatecommand=(self.master.register(only_numbers), "%S"))

        self.t1_label = ttk.Label(self.params_frame, text="Czas początkowy t1: ")
        self.t1_entry = ttk.Entry(self.params_frame, validate="key",
                                  validatecommand=(self.master.register(only_numbers), "%S"))

        self.d_label = ttk.Label(self.params_frame, text="Czas trwania sygnału d: ")
        self.d_entry = ttk.Entry(self.params_frame, validate="key",
                                 validatecommand=(self.master.register(only_numbers), "%S"))

        self.T_label = ttk.Label(self.params_frame, text="Okres podstawowy T: ")
        self.T_entry = ttk.Entry(self.params_frame, validate="key",
                                 validatecommand=(self.master.register(only_numbers), "%S"))

        self.kw_label = ttk.Label(self.params_frame, text="Współczynnik kw: ")
        self.kw_entry = ttk.Entry(self.params_frame, validate="key",
                                  validatecommand=(self.master.register(only_numbers), "%S"))

        self.ts_label = ttk.Label(self.params_frame, text="Czas skoku ts: ")
        self.ts_entry = ttk.Entry(self.params_frame, validate="key",
                                  validatecommand=(self.master.register(only_numbers), "%S"))

        self.ns_label = ttk.Label(self.params_frame, text="Numer próbki skoku ns: ")
        self.ns_entry = ttk.Entry(self.params_frame, validate="key",
                                  validatecommand=(self.master.register(only_numbers), "%S"))

        self.p_label = ttk.Label(self.params_frame, text="Prawdopodobieństwo p: ")
        self.p_entry = ttk.Entry(self.params_frame, validate="key",
                                 validatecommand=(self.master.register(only_numbers), "%S"))

        self.h_label = ttk.Label(self.params_frame, text="Liczba przedziałów histogramu: ")
        self.h_entry = ttk.Entry(self.params_frame, validate="key",
                                 validatecommand=(self.master.register(only_numbers), "%S"))

    def show_params(self, *args):
        for widget in self.params_frame.winfo_children():
            widget.grid_forget()
        self.f_label.grid(column=0, row=0)
        self.f_entry.grid(column=1, row=0)
        self.A_label.grid(column=0, row=1)
        self.A_entry.grid(column=1, row=1)
        self.t1_label.grid(column=0, row=2)
        self.t1_entry.grid(column=1, row=2)
        self.d_label.grid(column=0, row=3)
        self.d_entry.grid(column=1, row=3)
        self.T_label.grid(column=0, row=4)
        self.T_entry.grid(column=1, row=4)

        self.h_entry.grid(column=1, row=6)
        self.h_label.grid(column=0, row=6)

        if self.selected_signal.get() in ["Sygnał prostokątny", "Sygnał prostokątny symetryczny", "Sygnał trójkątny"]:
            self.kw_label.grid(column=0, row=5)
            self.kw_entry.grid(column=1, row=5)
        elif self.selected_signal.get() == "Skok jednostkowy":
            self.ts_label.grid(column=0, row=5)
            self.ts_entry.grid(column=1, row=5)
        elif self.selected_signal.get() == "Impuls jednostkowy":
            self.ns_label.grid(column=0, row=5)
            self.ns_entry.grid(column=1, row=5)
        elif self.selected_signal.get() == "Szum impulsowy":
            self.p_label.grid(column=0, row=5)
            self.p_entry.grid(column=1, row=5)
        self.frame.update_idletasks()

    def create_signal(self):
        signal = signal_map.get(self.selected_signal.get())
        if signal in [analog_signal.S1, analog_signal.S2]:
            return signal(float(self.A_entry.get()), float(self.t1_entry.get()), float(self.d_entry.get()),
                          float(self.T_entry.get()))
        elif signal in [analog_signal.S3, analog_signal.S4, analog_signal.S5]:
            return signal(float(self.A_entry.get()), float(self.t1_entry.get()), float(self.d_entry.get()),
                          float(self.T_entry.get()))
        elif signal in [analog_signal.S6, analog_signal.S7, analog_signal.S8]:
            return signal(float(self.A_entry.get()), float(self.t1_entry.get()), float(self.d_entry.get()),
                          float(self.T_entry.get()), float(self.kw_entry.get()))
        elif signal == analog_signal.S9:
            return signal(float(self.A_entry.get()), float(self.t1_entry.get()), float(self.d_entry.get()),
                          float(self.T_entry.get()), float(self.ts_entry.get()))
        elif signal == analog_signal.S10:
            return signal(float(self.A_entry.get()), float(self.ns_entry.get()))
        elif signal == analog_signal.S11:
            return signal(float(self.A_entry.get()), float(self.p_entry.get()))
        else:
            return None

    def plot_signal(self, signal: analog_signal.AnalogSignal):
        if isinstance(signal, analog_signal.DiscreteAnalogSignal):
            samples = int((int(self.d_entry.get()) - int(self.t1_entry.get())) * int(self.f_entry.get()))
            sig = signal_conversion.discrete_sampling(signal, samples)
        elif isinstance(signal, analog_signal.ContinuousAnalogSignal):
            sig = signal_conversion.uniform_sampling(signal, int(self.f_entry.get()),
                                                     float(self.t1_entry.get()),
                                                     float(self.t1_entry.get() + self.d_entry.get()))
        else:
            raise ValueError("Niepoprawny sygnał")

        fig = plt.figure()
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)

        if isinstance(signal, analog_signal.S10) or isinstance(signal, analog_signal.S11):
            ax1.scatter(sig.time, sig.samples, s=1)
        else:
            ax1.plot(sig.time, sig.samples)

        ax2.hist(sig.samples, bins=int(self.h_entry.get()), edgecolor='black')
        return fig

    def generate_btn(self):
        self.close_other()
        signal = self.create_signal()
        fig = self.plot_signal(signal)
        sig = None
        self.current_analog = signal
        if isinstance(signal, analog_signal.DiscreteAnalogSignal):
            samples = int((int(self.d_entry.get()) - int(self.t1_entry.get())) * int(self.f_entry.get()))
            sig = signal_conversion.discrete_sampling(signal, samples)
        elif isinstance(signal, analog_signal.ContinuousAnalogSignal):
            sig = signal_conversion.uniform_sampling(signal, int(self.f_entry.get()),
                                                     float(self.t1_entry.get()),
                                                     float(self.t1_entry.get() + self.d_entry.get()))
        if sig is None:
            raise ValueError("Niepoprawny sygnał")
        self.show_info(fig, sig)

    def load_from_file(self):
        self.close_other()
        filename = self.file_name_entry.get() + '.bin'
        sig = digital_signal.DigitalSignal(file_path=filename)

        fig = plt.figure()
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)

        ax1.plot(sig.time, sig.samples)
        ax2.hist(sig.samples, 10, edgecolor='black')
        self.show_info(fig, sig)

    def show_info(self, fig, sig: digital_signal.DigitalSignal):
        self.current = sig
        new_window = Toplevel(self.master)
        self.windows.append(new_window)
        new_window.title(self.title)
        new_frame = SignalInfoFrame(new_window, sig.samples, fig, sig.sampling_rate, sig.start_time, len(sig.samples))
        new_frame.frame.grid(column=0, row=0)

    def close_other(self):
        for window in self.windows:
            window.destroy()
        self.windows.clear()
