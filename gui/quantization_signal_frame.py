from tkinter import ttk, StringVar, Toplevel

from matplotlib import pyplot as plt

from signal_info_frame import SignalInfoFrame
from plot_creation_frame import PlotCreationFrame

from api import digital_signal, signal_conversion


class QuantizationSignalFrame:
    def __init__(self, master, function_frame1: PlotCreationFrame):
        self.master = master
        self.function_frame1 = function_frame1
        self.frame = ttk.Frame(self.master, padding="10")
        self.windows = []
        self.signal_to_quantize = None
        self.time = []
        self.samples = []

        self.selected_quantization = StringVar()
        self.init_op_dropdown_quan()

        ttk.Button(self.frame, text="Wykonaj kwantyzację", command=self.execute_quantization).grid(column=1, row=0)

        self.selected_reconstruction = StringVar()
        self.init_op_dropdown_recon()

        ttk.Button(self.frame, text="Wykonaj rekonstrukcje", command=self.execute_reconstruction).grid(column=1, row=1)

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

    def execute_quantization(self):
        self.close_other()
        self.signal_to_quantize = digital_signal.DigitalSignal(None, self.function_frame1.current.start_time,
                                                               self.function_frame1.current.sampling_rate,
                                                               self.function_frame1.current.samples,
                                                               self.function_frame1.current.time)
        quantized = None

        quantization = self.selected_quantization.get()
        if quantization == "Kwantyzacja równomierna z zaokrągleniem":
            quantized = signal_conversion.uniform_quantization(self.signal_to_quantize)
            self.time = quantized.time
            self.samples = quantized.samples

        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)

        ax1.plot(self.function_frame1.current.time, self.function_frame1.current.samples)
        ax2.plot(quantized.time, quantized.samples)

        self.show_info(quantized.samples, fig, quantized, quantized.start_time,
                       quantized.samples, "Kwantyzacja")

    def execute_reconstruction(self):
        self.close_other()
        signal_to_reconstruct = self.signal_to_quantize

        reconstruction = self.selected_reconstruction.get()
        reconstructed = None

        if reconstruction == "Ekstrapolacja zerowego rzędu":
            reconstructed = signal_conversion.zero_order_extrapolation(signal_to_reconstruct)
        elif reconstruction == "Interpolacja pierwszego rzędu":
            reconstructed = signal_conversion.first_order_extrapolation(signal_to_reconstruct)
        elif reconstruction == "Rekonstrukcja w oparciu o funkcje sinc":
            reconstructed = signal_conversion.sinc_extrapolation(signal_to_reconstruct)

        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)

        ax1.plot(self.time, self.samples)
        ax2.plot(reconstructed.time, reconstructed.samples)

        self.show_info(reconstructed.samples, fig, reconstructed.sampling_rate, reconstructed.start_time,
                       reconstructed.samples, "Rekonstrukcja")