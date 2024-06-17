# GUI setup
import time
import pickle
import tkinter.filedialog
import tkinter
from tkinter import Tk, ttk

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from zad4.api import signal_conversion, operations
from zad4.gui.filter_creator import filter_creator_frame
from zad4.gui.signal_frame import SignalGenerator

operations_window = None
zad3_window = None

root = Tk()
root.title("CPS - Zadanie 4")
main_frame = ttk.Frame(root, padding="10")
s1Frame = ttk.Frame(main_frame)
s1 = SignalGenerator(s1Frame)
s1.frame.pack()
s1Frame.pack(side='left')


def execute_operation(s2, param):
    signal1 = s1.y_values
    signal2 = s2.y_values

    num_samples_1 = int(float(s1.duration_entry.get()) * int(s1.sampling_frequency_entry.get()))
    num_samples_2 = int(float(s2.duration_entry.get()) * int(s2.sampling_frequency_entry.get()))

    y1 = signal_conversion.real_sampling(signal1, num_samples_1)
    y2 = signal_conversion.real_sampling(signal2, num_samples_2)

    if param == "add":
        s1.y_values = operations.add(y1, y2)
    elif param == "sub":
        s1.y_values = operations.sub(y1, y2)
    elif param == "mul":
        s1.y_values = operations.mul(y1, y2)
    elif param == "div":
        s1.y_values = operations.div(y1, y2)

    s1.t_values = np.linspace(s1.t_values[0], s1.t_values[-1], len(s1.y_values))
    s1.show_plot("", "plot")
    operations_window.destroy()


def open_window_operation(param):
    title = ""
    if param == "add":
        title = "Dodawanie"
    elif param == "sub":
        title = "Odejmowanie"
    elif param == "mul":
        title = "Mnożenie"
    elif param == "div":
        title = "Dzielenie"
    global operations_window
    if operations_window is not None:
        operations_window.destroy()
    operations_window = tkinter.Toplevel(main_frame)
    operations_window.title(title)
    s2 = SignalGenerator(operations_window)
    s2.frame.pack()
    ttk.Button(operations_window, text="Wykonaj operację", command=lambda: execute_operation(s2, param)).pack()


# Operations line

operations_frame = ttk.Frame(main_frame)
ttk.Button(operations_frame, text="Dodawanie", command=lambda: open_window_operation("add")).pack(side='left')
ttk.Button(operations_frame, text="Odejmowanie", command=lambda: open_window_operation("sub")).pack(side='left')
ttk.Button(operations_frame, text="Mnożenie", command=lambda: open_window_operation("mul")).pack(side='left')
ttk.Button(operations_frame, text="Dzielenie", command=lambda: open_window_operation("div")).pack(side='left')
operations_frame.pack(side='top')

ttk.Separator(main_frame, orient='horizontal').pack(fill='x', side='top')


def open_window_convolution():
    global zad3_window
    if zad3_window is not None:
        zad3_window.destroy()
    zad3_window = tkinter.Toplevel(main_frame)
    zad3_window.title("Splot")
    s2 = SignalGenerator(zad3_window)
    s2.frame.pack()
    ttk.Button(zad3_window, text="Wykonaj splot", command=lambda: execute_convolution(s2)).pack()


def open_window_correlation():
    global zad3_window
    if zad3_window is not None:
        zad3_window.destroy()
    zad3_window = tkinter.Toplevel(main_frame)
    zad3_window.title("Korelacja")
    s2 = SignalGenerator(zad3_window)
    s2.frame.pack()
    ttk.Button(zad3_window, text="Wykonaj korelacje", command=lambda: execute_correlation(s2)).pack()


def execute_convolution(s2):
    signal1 = s1.y_values
    signal2 = s2.y_values

    num_samples_1 = int(float(s1.duration_entry.get()) * int(s1.sampling_frequency_entry.get()))
    num_samples_2 = int(float(s2.duration_entry.get()) * int(s2.sampling_frequency_entry.get()))

    y1 = signal_conversion.real_sampling(signal1, num_samples_1)
    y2 = signal_conversion.real_sampling(signal2, num_samples_2)

    s1.y_values = operations.convolution(y1, y2)
    s1.t_values = np.linspace(s1.t_values[0], s1.t_values[-1], len(s1.y_values))
    s1.show_plot("", "plot")
    zad3_window.destroy()


def execute_correlation(s2):
    signal1 = s1.y_values
    signal2 = s2.y_values

    num_samples_1 = int(float(s1.duration_entry.get()) * int(s1.sampling_frequency_entry.get()))
    num_samples_2 = int(float(s2.duration_entry.get()) * int(s2.sampling_frequency_entry.get()))

    y1 = signal_conversion.real_sampling(signal1, num_samples_1)
    y2 = signal_conversion.real_sampling(signal2, num_samples_2)

    s1.y_values = operations.correlation_convolve(y1, y2)
    s1.t_values = np.linspace(s1.t_values[0], s1.t_values[-1], len(s1.y_values))
    s1.show_plot("", "plot")
    zad3_window.destroy()


zad3_operations_frame = ttk.Frame(main_frame)
ttk.Button(zad3_operations_frame, text="Splot", command=lambda: open_window_convolution()).pack(side='left')
ttk.Button(zad3_operations_frame, text="Korelacja", command=lambda: open_window_correlation()).pack(side='left')
zad3_operations_frame.pack(side='top')


def execute_filtration(filterwindow):
    s1.y_values = operations.convolution(s1.y_values, filterwindow.y_values)
    s1.t_values = np.linspace(s1.t_values[0], s1.t_values[-1], len(s1.y_values))
    s1.show_plot("", "plot")


def execute_create_filter_window():
    global zad3_window
    if zad3_window is not None:
        zad3_window.destroy()
    new_window = tkinter.Toplevel(main_frame)
    new_window.title("Tworzenie filtru")
    filterwindow = filter_creator_frame(new_window)
    filterwindow.frame.pack()
    ttk.Button(new_window, text="Wykonaj filtracje", command=lambda: execute_filtration(filterwindow)).pack()


ttk.Button(zad3_operations_frame, text="Filtr", command=lambda: execute_create_filter_window()).pack(side='left')
zad3_operations_frame.pack()

########################################


def prepare_output(y_values: []):
    real_parts = [val.real for val in y_values]
    imag_parts = [val.imag for val in y_values]
    magnitudes = [abs(val) for val in y_values]
    phases = [np.arctan2(val.imag, val.real) for val in y_values]
    return real_parts, imag_parts, magnitudes, phases


def plot_complex_signal(y_values: [], mode='W1'):
    N = len(y_values)
    frequencies = np.arange(N)

    real_parts, imag_parts, magnitudes, phases = prepare_output(y_values)
    fig = None

    if mode == 'W1':
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

        # Upper plot (real part vs frequency)
        ax1.plot(frequencies, real_parts, label='Real part')
        ax1.set_ylabel('Real part amplitude')
        ax1.legend()

        # Lower plot (imaginary part vs frequency)
        ax2.plot(frequencies, imag_parts, label='Imaginary part')
        ax2.set_xlabel('Frequency')
        ax2.set_ylabel('Imaginary part amplitude')
        ax2.legend()

        plt.suptitle('Frequency Domain Representation (W1)')

    elif mode == 'W2':
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

        # Upper plot (magnitude vs frequency)
        ax1.plot(frequencies, magnitudes, label='Magnitude')
        ax1.set_ylabel('Magnitude')
        ax1.legend()

        # Lower plot (phase vs frequency)
        ax2.plot(frequencies, phases, label='Phase')
        ax2.set_xlabel('Frequency')
        ax2.set_ylabel('Phase')
        ax2.legend()

        plt.suptitle('Frequency Domain Representation (W2)')
    elif mode == 'COS' or mode == 'WH':
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Magnitude')
        plt.plot(frequencies, y_values, label='Magnitude')

    return fig


def execute_transformation(param):
    start_time = time.time()
    end_time = 0
    if param == "DFT":
        s1.y_values = operations.discrete_transformation_Fourier(s1.y_values)
        end_time = time.time()
        exec_time = end_time - start_time
        fig1 = plot_complex_signal(s1.y_values, 'W1')
        fig2 = plot_complex_signal(s1.y_values, 'W2')
        show_plots_in_gui(fig1, exec_time)
        show_plots_in_gui(fig2, exec_time)
    elif param == "FFT":
        s1.y_values = operations.fast_discrete_fourier_transform(s1.y_values)
        end_time = time.time()
        exec_time = end_time - start_time
        fig1 = plot_complex_signal(s1.y_values, 'W1')
        fig2 = plot_complex_signal(s1.y_values, 'W2')
        show_plots_in_gui(fig1, exec_time)
        show_plots_in_gui(fig2, exec_time)
    elif param == "DCT II":
        s1.y_values = operations.discrete_cosine_transform(s1.y_values)
        end_time = time.time()
        exec_time = end_time - start_time
        fig = plot_complex_signal(s1.y_values, 'COS')
        show_plots_in_gui(fig, exec_time)
    elif param == "WHT":
        s1.y_values = operations.walsh_hadamard_transform(s1.y_values)
        end_time = time.time()
        exec_time = end_time - start_time
        fig = plot_complex_signal(s1.y_values, 'WH')
        show_plots_in_gui(fig, exec_time)
    s1.t_values = np.linspace(s1.t_values[0], s1.t_values[-1], len(s1.y_values))
    s1.show_plot("", "plot")


def save_parameters_to_file():
    filename = tkinter.filedialog.asksaveasfilename(defaultextension=".pkl",
                                                    filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")],
                                                    title="Save Parameters")
    if filename:
        parameters = {
            't_values': s1.t_values,
            'y_values': s1.y_values
        }
        with open(filename, 'wb') as f:
            pickle.dump(parameters, f)


def load_parameters_from_file():
    filename = tkinter.filedialog.askopenfilename(filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")],
                                                  title="Load Parameters")
    if filename:
        with open(filename, 'rb') as f:
            parameters = pickle.load(f)
            s1.t_values = parameters['t_values']
            s1.y_values = parameters['y_values']
            s1.show_plot("", "plot")


def show_plots_in_gui(fig, exec_time):
    window = tkinter.Toplevel(main_frame)
    window.title("Wykres")
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=1)
    canvas.get_tk_widget().grid(column=0, row=0)
    ttk.Label(window, text="Czas wykonania: " + str(round(exec_time, 5))).grid(column=0, row=1)

########################################


transformation_frame = ttk.Frame(main_frame)
ttk.Separator(main_frame, orient='horizontal').pack(fill='x', side='top')
ttk.Button(transformation_frame, text="DFT", command=lambda: execute_transformation("DFT")).pack(side='left')
ttk.Button(transformation_frame, text="FFT", command=lambda: execute_transformation("FFT")).pack(side='left')
ttk.Button(transformation_frame, text="DCT II", command=lambda: execute_transformation("DCT II")).pack(side='left')
ttk.Button(transformation_frame, text="TWH", command=lambda: execute_transformation("WHT")).pack(side='left')
transformation_frame.pack(side='top')
ttk.Separator(main_frame, orient='horizontal').pack(fill='x', side='top')

file_frame = ttk.Frame(main_frame)
ttk.Button(file_frame, text="Wczytaj z pliku", command=lambda: load_parameters_from_file()).pack(side='left')
ttk.Button(file_frame, text="Zapisz do pliku", command=lambda: save_parameters_to_file()).pack(side='left')
file_frame.pack(side='top')

main_frame.pack()
root.mainloop()
