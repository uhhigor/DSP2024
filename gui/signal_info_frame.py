from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import Signal


class SignalInfoFrame:
    def __init__(self, master, signal: Signal, samples, fig):
        self.master = master
        self.frame = ttk.Frame(self.master, padding="10")
        self.signal = signal
        self.fig = fig
        self.init_widgets()
        self.show(signal, samples)

    def init_widgets(self):
        self.avg_label = ttk.Label(self.frame, text="Wartość średnia sygnału: ")
        self.avg_label.grid(column=0, row=1)
        self.avg_label_value = ttk.Label(self.frame, text="")
        self.avg_label_value.grid(column=1, row=1)
        self.avg_abs_label = ttk.Label(self.frame, text="Wartość średnia bezwzględna sygnału: ")
        self.avg_abs_label.grid(column=0, row=2)
        self.avg_abs_label_value = ttk.Label(self.frame, text="")
        self.avg_abs_label_value.grid(column=1, row=2)
        self.avg_power_label = ttk.Label(self.frame, text="Moc średnia sygnału: ")
        self.avg_power_label.grid(column=0, row=3)
        self.avg_power_label_value = ttk.Label(self.frame, text="")
        self.avg_power_label_value.grid(column=1, row=3)
        self.variance_label = ttk.Label(self.frame, text="Wariancja sygnału: ")
        self.variance_label.grid(column=0, row=4)
        self.variance_label_value = ttk.Label(self.frame, text="")
        self.variance_label_value.grid(column=1, row=4)
        self.effective_label = ttk.Label(self.frame, text="Wartość skuteczna sygnału: ")
        self.effective_label.grid(column=0, row=5)
        self.effective_label_value = ttk.Label(self.frame, text="")
        self.effective_label_value.grid(column=1, row=5)

    def show(self, signal: Signal, samples):
        if signal is not None:
            if signal is Signal.S10 or signal is Signal.S11:
                self.avg_label_value.config(text=str(round(signal.discrete_average_value(signal, samples), 3)))
                self.avg_abs_label_value.config(text=str(round(signal.discrete_average_value_absolute(signal, samples), 3)))
                self.avg_power_label_value.config(text=str(round(signal.discrete_average_power(signal, samples), 3)))
                self.variance_label_value.config(text=str(round(signal.discrete_variance(signal, samples), 3)))
                self.effective_label_value.config(text=str(round(signal.discrete_effective_value(signal, samples), 3)))
            else:
                self.avg_label_value.config(text=str(round(signal.continuous_average_value(signal), 3)))
                self.avg_abs_label_value.config(text=str(round(signal.continuous_average_value_absolute(signal), 3)))
                self.avg_power_label_value.config(text=str(round(signal.continuous_average_power(signal), 3)))
                self.variance_label_value.config(text=str(round(signal.continuous_variance(signal), 3)))
                self.effective_label_value.config(text=str(round(signal.continuous_effective_value(signal), 3)))
        canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().grid(column=0, row=6, columnspan=2)
        self.frame.grid(column=0, row=0, columnspan=2, rowspan=6)
