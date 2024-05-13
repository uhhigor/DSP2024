from tkinter import ttk, StringVar

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from api import signal_parameters
from api import signal_conversion


class SignalInfoFrame:
    def __init__(self, master, y_values, t_values, frequency, start_time, num_samples):
        self.selected_reconstruction = None
        self.selected_quantization = None
        self.number_of_samples_entry = None
        self.number_of_samples = None
        self.master = master
        self.frame = ttk.Frame(self.master, padding="10")
        self.init_y_values = y_values
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

        self.mse_label = ttk.Label(self.frame, text="Błąd średniokwadratowy: ")
        self.mse_label_value = ttk.Label(self.frame, text="")
        self.snr_label = ttk.Label(self.frame, text="Stosunek sygnał-szum: ")
        self.snr_label_value = ttk.Label(self.frame, text="")
        self.md_label = ttk.Label(self.frame, text="Maksymalna różnica: ")
        self.md_label_value = ttk.Label(self.frame, text="")

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

        self.mse_label.grid(column=2, row=6)
        self.mse_label_value.grid(column=3, row=6)
        self.snr_label.grid(column=2, row=7)
        self.snr_label_value.grid(column=3, row=7)
        self.md_label.grid(column=2, row=8)
        self.md_label_value.grid(column=3, row=8)

    def show(self, y_values, t_values, type="plot", color="blue"):
        self.avg_label_value.config(text=str(round(signal_parameters.average_value(y_values), 3)))
        self.avg_abs_label_value.config(text=str(round(signal_parameters.average_value_absolute(y_values), 3)))
        self.avg_power_label_value.config(text=str(round(signal_parameters.average_power(y_values), 3)))
        self.variance_label_value.config(text=str(round(signal_parameters.continuous_variance(y_values), 3)))
        self.effective_label_value.config(text=str(round(signal_parameters.continuous_effective_value(y_values), 3)))
        plot = plt.figure()
        ax1 = plot.add_subplot(211)
        ax2 = plot.add_subplot(212)
        if type == "plot":
            ax1.plot(t_values, y_values, color=color)
            ax2.hist(y_values, bins=10, edgecolor='black', color='gray')
        elif type == "scatter":
            display_y = []
            display_t = []
            number_of_samples = self.num_samples / int(self.number_of_samples.get())
            for i in range(0, len(y_values), int(number_of_samples)):
                display_y.append(y_values[i])
                display_t.append(t_values[i])
            ax1.scatter(display_t, display_y, 5, color=color)
            ax2.hist(display_y, bins=10, edgecolor='black',  color='gray')
        canvas = FigureCanvasTkAgg(plot, master=self.frame)
        canvas.draw()
        if color == "red":
            canvas.get_tk_widget().grid(column=2, row=9, columnspan=2)
        else:
            canvas.get_tk_widget().grid(column=0, row=9, columnspan=2)
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

    def calculate_measurements(self, y_values, y1_values):
        self.mse_label_value.config(text=str(round(signal_parameters.mean_square_error(y_values, y1_values), 3)))
        self.snr_label_value.config(text=str(round(signal_parameters.signal_to_noise_ratio(y_values, y1_values), 3)))
        self.md_label_value.config(text=str(round(signal_parameters.maximum_difference(y_values, y1_values), 3)))

    def execute_sampling(self):
        sampled_y = signal_conversion.conversion_sampling(self.init_y_values, int(self.number_of_samples.get()))
        self.y_values = sampled_y
        self.show(self.init_y_values, self.t_values)
        self.show(self.y_values, self.t_values, "scatter", "red")
        self.calculate_measurements(self.init_y_values, self.y_values)

    def execute_quantization(self):
        quantized = signal_conversion.uniform_quantization(self.y_values)
        self.y_values = quantized
        self.show(self.init_y_values, self.t_values)
        self.show(self.y_values, self.t_values, "plot", "red")
        self.calculate_measurements(self.init_y_values, self.y_values)

    def execute_reconstruction(self):
        reconstructed = None
        if self.selected_reconstruction.get() == "Ekstrapolacja zerowego rzędu":
            reconstructed = signal_conversion.zero_order_extrapolation(self.y_values,
                                                                       int(self.number_of_samples.get()))
        elif self.selected_reconstruction.get() == "Interpolacja pierwszego rzędu":
            reconstructed = signal_conversion.first_order_extrapolation(self.y_values,
                                                                        int(self.number_of_samples.get()))
        elif self.selected_reconstruction.get() == "Rekonstrukcja w oparciu o funkcje sinc":
            reconstructed = signal_conversion.sinc_extrapolation(self.y_values, int(self.number_of_samples.get()))
        self.y_values = reconstructed
        self.show(self.init_y_values, self.t_values)
        self.show(self.y_values, self.t_values, "plot", "red")
        self.calculate_measurements(self.init_y_values, self.y_values)

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
