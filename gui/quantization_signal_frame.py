from tkinter import ttk, StringVar, Toplevel

from matplotlib import pyplot as plt

from api import signal_conversion
from plot_creation_frame import PlotCreationFrame
from signal_info_frame import SignalInfoFrame


class QuantizationSignalFrame:
    def __init__(self, master, function_frame1: PlotCreationFrame):
        self.master = master
        self.function_frame1 = function_frame1
        self.frame = ttk.Frame(self.master, padding="10")
        self.windows = []
        self.sampled = None
        self.quantized = None
        self.reconstructed = None
        self.time = []
        self.samples = []

        self.selected_sampling = StringVar()

        ttk.Button(self.frame, text="Wykonaj próbkowanie", command=self.execute_sampling).grid(column=1, row=0)
        self.number_of_samples = StringVar()
        self.number_of_samples_entry = ttk.Entry(self.frame, textvariable=self.number_of_samples)
        self.number_of_samples_entry.grid(column=2, row=0)

        self.selected_quantization = StringVar()
        self.init_op_dropdown_quan()

        ttk.Button(self.frame, text="Wykonaj kwantyzację", command=self.execute_quantization).grid(column=1, row=1)

        self.selected_reconstruction = StringVar()
        self.init_op_dropdown_recon()

        ttk.Button(self.frame, text="Wykonaj rekonstrukcje", command=self.execute_reconstruction).grid(column=1, row=2)

    def init_op_dropdown_quan(self):
        quantization = ["None", "Kwantyzacja równomierna z zaokrągleniem"]
        dropdown_quantization = ttk.OptionMenu(self.frame, self.selected_quantization, *quantization)
        dropdown_quantization.grid(column=5, row=0)
        self.selected_quantization.set("Kwantyzacja równomierna z zaokrągleniem")

    def init_op_dropdown_recon(self):
        reconstructions = ["None", "Ekstrapolacja zerowego rzędu", "Interpolacja pierwszego rzędu",
                           "Rekonstrukcja w oparciu o funkcje sinc"]
        dropdown_reconstruction = ttk.OptionMenu(self.frame, self.selected_reconstruction, *reconstructions)
        dropdown_reconstruction.grid(column=5, row=1)
        self.selected_reconstruction.set("Ekstrapolacja zerowego rzędu")

    def show_info(self, y_values, fig, f, t1, samples, title):
        new_window = Toplevel(self.master)
        self.windows.append(new_window)
        new_window.title(title)
        new_frame = SignalInfoFrame(new_window, y_values, fig, f, t1, samples)
        new_frame.frame.grid(column=0, row=0)

    def close_other(self):
        for window in self.windows:
            window.destroy()
        self.windows.clear()

    def execute_sampling(self):
        self.close_other()
        self.current_signal = self.function_frame1.current
        number_of_samples = int(self.number_of_samples.get())

        sampled = signal_conversion.conversion_sampling(self.current_signal, number_of_samples)

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        self.sampled = sampled
        ax1.plot(self.function_frame1.current.time, self.function_frame1.current.samples)
        ax1.scatter(self.sampled.time, self.sampled.samples)

        self.show_info(sampled.samples, fig, sampled.sampling_rate, sampled.start_time, sampled.samples, "Próbkowanie")

    def execute_quantization(self):
        self.close_other()
        quantized = None

        quantization = self.selected_quantization.get()
        if quantization == "Kwantyzacja równomierna z zaokrągleniem":
            quantized = signal_conversion.uniform_quantization(self.sampled)
            self.time = quantized.time
            self.samples = quantized.samples

        fig = plt.figure()
        ax1 = fig.add_subplot(111)

        self.quantized = quantized
        ax1.plot(self.function_frame1.current.time, self.function_frame1.current.samples)
        ax1.scatter(self.sampled.time, self.sampled.samples)
        ax1.scatter(self.quantized.time, self.quantized.samples)

        self.show_info(quantized.samples, fig, quantized, quantized.start_time,
                       quantized.samples, "Kwantyzacja")

    def execute_reconstruction(self):
        self.close_other()
        signal_to_reconstruct = self.quantized

        reconstruction = self.selected_reconstruction.get()
        reconstructed = None

        if reconstruction == "Ekstrapolacja zerowego rzędu":
            reconstructed = signal_conversion.zero_order_extrapolation(signal_to_reconstruct)
        elif reconstruction == "Interpolacja pierwszego rzędu":
            reconstructed = signal_conversion.first_order_extrapolation(signal_to_reconstruct)
        elif reconstruction == "Rekonstrukcja w oparciu o funkcje sinc":
            reconstructed = signal_conversion.sinc_extrapolation(signal_to_reconstruct)

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.plot(self.function_frame1.current.time, self.function_frame1.current.samples)
        ax1.plot(reconstructed.time, reconstructed.samples)

        self.reconstructed = reconstructed

        self.show_info(reconstructed.samples, fig, reconstructed.sampling_rate, reconstructed.start_time,
                       reconstructed.samples, "Rekonstrukcja")
