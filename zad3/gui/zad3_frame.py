from tkinter import ttk, StringVar

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from zad3.api import signal_zad3, signal_conversion
from zad3.gui.filter_creator import filter_creator_frame


class zad3Frame:
    def __init__(self, master, s1Frame, s2Frame):
        self.y_values = None
        self.t_values = None
        self.frame = ttk.Frame(master, padding="10")
        self.s1Frame = s1Frame
        self.s2Frame = s2Frame

        self.filter_creator = None

        # Generate convolution button
        ttk.Button(self.frame, text="Wykonaj splot", command=lambda: self.execute_convolution()).grid(
            column=0, row=2, columnspan=2)


        ttk.Button(self.frame, text="Utwórz filtr", command=lambda: self.execute_create_filter_window()).grid(
            column=0, row=4, columnspan=2)

        ttk.Button(self.frame, text="Filtruj", command=lambda: self.execute_filtration()).grid(
            column=0, row=5, columnspan=2)



        fig, self.ax = plt.subplots()
        self.ax.figure.set_size_inches(2, 1.5)
        self.ax.tick_params(axis='both', labelsize=3)
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=3, columnspan=2)

    def execute_convolution(self):
        signal1 = self.s1Frame.y_values
        signal2 = self.s2Frame.y_values

        num_samples_1 = int(float(self.s1Frame.duration_entry.get()) * int(self.s1Frame.sampling_frequency_entry.get()))
        num_samples_2 = int(float(self.s2Frame.duration_entry.get()) * int(self.s2Frame.sampling_frequency_entry.get()))

        y1 = signal_conversion.real_sampling(signal1, num_samples_1)
        y2 = signal_conversion.real_sampling(signal2, num_samples_2)

        self.y_values = signal_zad3.convolution(y1, y2)
        self.t_values = np.linspace(self.s1Frame.t_values[0], self.s1Frame.t_values[-1], len(self.y_values))
        self.show_plot("Splot", self.t_values, self.y_values)

    def execute_filtration(self):
        filter_y_values = self.filter_creator.y_values
        self.y_values = np.convolve(self.y_values, filter_y_values, mode="same")
        #self.t_values = np.linspace(self.s1Frame.t_values[0], self.s1Frame.t_values[-1], len(self.y_values))
        self.show_plot("Filtracja", self.t_values, self.y_values)

    def show_plot(self, title: str, t_values, y_values, clear: bool = True):
        if clear:
            self.ax.clear()
            self.canvas.draw()
        self.ax.set_title(title, fontsize=6)
        self.ax.plot(t_values, y_values, linewidth=0.5)
        self.canvas.draw()

    def execute_create_filter_window(self):
        self.filter_creator = filter_creator_frame(self.frame)