from tkinter import ttk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import Signal
import SignalParameters


class SignalInfoFrame:
    def __init__(self, master, y_values, fig, frequency, start_time, num_samples):
        self.master = master
        self.frame = ttk.Frame(self.master, padding="10")
        self.y_values = y_values
        self.fig = fig
        self.frequency = frequency
        self.start_time = start_time
        self.num_samples = num_samples
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

        self.save_button = ttk.Button(self.frame, text="Zapisz do pliku", command=self.save_to_file)
        self.save_button.grid(column=0, row=7)
        self.file_name_label = ttk.Label(self.frame, text="Nazwa pliku: ")
        self.file_name_label.grid(column=0, row=8)
        self.file_name_entry = ttk.Entry(self.frame)
        self.file_name_entry.grid(column=1, row=8)
        self.file_name_entry.insert(0, "signal")

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

    def save_to_file(self):
        params = {
            'start_time': self.start_time,
            'sampling_frequency': self.frequency,
            'num_samples': self.num_samples,
        }
        filename = self.file_name_entry.get()+'.bin'
        y_array = np.array(self.y_values, dtype=np.float64)
        with open(filename, 'wb') as file:
            file.write(np.array([params['start_time']], dtype=np.float64).tobytes())
            file.write(np.array([params['sampling_frequency']], dtype=np.float64).tobytes())
            file.write(np.array([params['num_samples']], dtype=np.int32).tobytes())
            file.write(y_array.tobytes())
