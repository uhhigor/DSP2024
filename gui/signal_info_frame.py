from tkinter import ttk, StringVar

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from api import signal_parameters
from api import signal_conversion


class SignalInfoFrame:
    def __init__(self, master, y_values, t_values, frequency, start_time, num_samples):
        self.master = master
        self.frame = ttk.Frame(self.master, padding="10")
        self.y_values = y_values
        self.t_values = t_values
        self.frequency = frequency
        self.start_time = start_time
        self.num_samples = num_samples

        self.avg_label = ttk.Label(self.frame, text="Wartość średnia sygnału: ")
        self.avg_label_value = ttk.Label(self.frame, text="")
        self.avg_abs_label = ttk.Label(self.frame, text="Wartość średnia bezwzględna sygnału: ")
        self.avg_abs_label_value = ttk.Label(self.frame, text="")
        self.avg_power_label = ttk.Label(self.frame, text="Moc średnia sygnału: ")
        self.avg_power_label_value = ttk.Label(self.frame, text="")
        self.variance_label = ttk.Label(self.frame, text="Wariancja sygnału: ")
        self.variance_label_value = ttk.Label(self.frame, text="")
        self.effective_label = ttk.Label(self.frame, text="Wartość skuteczna sygnału: ")
        self.effective_label_value = ttk.Label(self.frame, text="")

        self.save_button = ttk.Button(self.frame, text="Zapisz do pliku", command=self.save_to_file)
        self.file_name_label = ttk.Label(self.frame, text="Nazwa pliku: ")
        self.file_name_entry = ttk.Entry(self.frame)

        self.init_widgets()
        self.show(y_values, t_values)
        self.show_buttons()

    def init_widgets(self):
        self.avg_label.grid(column=0, row=1)
        self.avg_label_value.grid(column=1, row=1)
        self.avg_abs_label.grid(column=0, row=2)
        self.avg_abs_label_value.grid(column=1, row=2)
        self.avg_power_label.grid(column=0, row=3)
        self.avg_power_label_value.grid(column=1, row=3)
        self.variance_label.grid(column=0, row=4)
        self.variance_label_value.grid(column=1, row=4)
        self.effective_label.grid(column=0, row=5)
        self.effective_label_value.grid(column=1, row=5)

        self.save_button.grid(column=0, row=7)
        self.file_name_label.grid(column=0, row=8)
        self.file_name_entry.grid(column=1, row=8)
        self.file_name_entry.insert(0, "signal")

    def show(self, y_values, t_values, type="plot"):
        self.avg_label_value.config(text=str(round(signal_parameters.average_value(y_values), 3)))
        self.avg_abs_label_value.config(text=str(round(signal_parameters.average_value_absolute(y_values), 3)))
        self.avg_power_label_value.config(text=str(round(signal_parameters.average_power(y_values), 3)))
        self.variance_label_value.config(text=str(round(signal_parameters.continuous_variance(y_values), 3)))
        self.effective_label_value.config(text=str(round(signal_parameters.continuous_effective_value(y_values), 3)))
        plot = plt.figure()
        if type == "plot":
            plt.plot(t_values, y_values)
        elif type == "scatter":
            plt.scatter(t_values, y_values, 5)
        canvas = FigureCanvasTkAgg(plot, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().grid(column=0, row=6, columnspan=2)
        self.frame.grid(column=0, row=0, columnspan=2, rowspan=6)

    def show_buttons(self):
        ttk.Button(self.frame, text="Wykonaj próbkowanie", command=self.execute_sampling).grid(column=2, row=2)
        self.number_of_samples = StringVar()
        self.number_of_samples_entry = ttk.Entry(self.frame, textvariable=self.number_of_samples)
        self.number_of_samples_entry.grid(column=3, row=2)

        self.selected_quantization = StringVar()

        ttk.Button(self.frame, text="Wykonaj kwantyzację", command=self.execute_quantization).grid(column=2, row=3)

        self.selected_reconstruction = StringVar()
        reconstructions = ["None", "Ekstrapolacja zerowego rzędu", "Interpolacja pierwszego rzędu",
                           "Rekonstrukcja w oparciu o funkcje sinc"]
        dropdown_reconstruction = ttk.OptionMenu(self.frame, self.selected_reconstruction, *reconstructions)
        dropdown_reconstruction.grid(column=3, row=4)
        self.selected_reconstruction.set("Ekstrapolacja zerowego rzędu")

        ttk.Button(self.frame, text="Wykonaj rekonstrukcje", command=self.execute_reconstruction).grid(column=2, row=4)

    def execute_sampling(self):
        sampled_y = signal_conversion.conversion_sampling(self.y_values, int(self.number_of_samples.get()))
        self.y_values = sampled_y
        self.show(self.y_values, self.t_values, "scatter")

    def execute_quantization(self):
        quantized = signal_conversion.uniform_quantization(self.y_values)
        self.y_values = quantized
        self.show(self.y_values, self.t_values, "scatter")
        pass

    def execute_reconstruction(self):
        reconstructed = None
        if self.selected_reconstruction.get() == "Ekstrapolacja zerowego rzędu":
            reconstructed = signal_conversion.zero_order_extrapolation(self.y_values, int(self.number_of_samples.get()))
        elif self.selected_reconstruction.get() == "Interpolacja pierwszego rzędu":
            reconstructed = signal_conversion.first_order_extrapolation(self.y_values, int(self.number_of_samples.get()))
        elif self.selected_reconstruction.get() == "Rekonstrukcja w oparciu o funkcje sinc":
            reconstructed = signal_conversion.sinc_extrapolation(self.y_values, int(self.number_of_samples.get()))
        self.y_values = reconstructed
        self.show(self.y_values, self.t_values)

    def save_to_file(self):
        params = {
            'start_time': self.start_time,
            'sampling_frequency': self.frequency,
            'num_samples': self.num_samples,
        }
        filename = self.file_name_entry.get() + '.bin'
        y_array = np.array(self.y_values, dtype=np.float64)
        with open(filename, 'wb') as file:
            file.write(np.array([params['start_time']], dtype=np.float64).tobytes())
            file.write(np.array([params['sampling_frequency']], dtype=np.float64).tobytes())
            file.write(np.array([params['num_samples']], dtype=np.int32).tobytes())
            file.write(y_array.tobytes())
