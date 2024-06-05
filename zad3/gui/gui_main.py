# GUI setup
import tkinter
from tkinter import Tk, ttk

import numpy as np

from zad3.api import signal_conversion, operations
from zad3.gui.filter_creator import filter_creator_frame
from zad3.gui.signal_frame import SignalGenerator

operations_window = None
zad3_window = None

root = Tk()
root.title("CPS - Zadanie 3")
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

main_frame.pack()
root.mainloop()
