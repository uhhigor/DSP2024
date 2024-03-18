from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import Signal
import SignalParameters


class SignalInfoFrame:
    def __init__(self, master, y_values, fig):
        self.master = master
        self.frame = ttk.Frame(self.master, padding="10")
        self.y_values = y_values
        self.fig = fig
        self.init_widgets()
        self.show(y_values)

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

    def show(self, y_values):
        self.avg_label_value.config(text=str(round(SignalParameters.average_value(y_values), 3)))
        self.avg_abs_label_value.config(text=str(round(SignalParameters.average_value_absolute(y_values), 3)))
        self.avg_power_label_value.config(text=str(round(SignalParameters.average_power(y_values), 3)))
        self.variance_label_value.config(text=str(round(SignalParameters.continuous_variance(y_values), 3)))
        self.effective_label_value.config(text=str(round(SignalParameters.continuous_effective_value(y_values), 3)))

        canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().grid(column=0, row=6, columnspan=2)
        self.frame.grid(column=0, row=0, columnspan=2, rowspan=6)
