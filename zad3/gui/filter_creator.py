import tkinter
from tkinter import ttk, StringVar

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from zad3.api import signal_zad3


class filter_creator_frame:
    def __init__(self, master):
        self.y_values = None
        self.t_values = None

        self.frame = ttk.Frame(master, padding="10")
        self.frame.pack()

        # Filtration
        ttk.Label(self.frame, text="Filtr ").grid(column=0, row=3)
        # type dropdown
        self.type_var = StringVar()
        ttk.OptionMenu(self.frame, self.type_var, "dolnoprzepustowy", "dolnoprzepustowy", "górnoprzepustowy").grid(
            column=1, row=3)
        ttk.Label(self.frame, text="Rząd filtru: ").grid(column=0, row=5)
        self.filter_m_entry = ttk.Entry(self.frame)
        self.filter_m_entry.insert(0, "100")
        self.filter_m_entry.grid(column=1, row=5)

        ttk.Label(self.frame, text="Częstotliwość odcięcia F0: ").grid(column=0, row=6)
        self.filter_f0_entry = ttk.Entry(self.frame)
        self.filter_f0_entry.insert(0, "1")
        self.filter_f0_entry.grid(column=1, row=6)
        ttk.Label(self.frame, text="Częstotliwość próbkowania Fd: ").grid(column=0, row=7)
        self.filter_fd_entry = ttk.Entry(self.frame)
        self.filter_fd_entry.insert(0, "100")
        self.filter_fd_entry.grid(column=1, row=7)
        # window dropdown
        self.window_var = StringVar()
        ttk.OptionMenu(self.frame, self.window_var, "Okno prostokątne", "Okno prostokątne", "Okno Hamminga").grid(
            column=0, row=8, columnspan=2)
        ttk.Button(self.frame, text="Generuj", command=lambda: self.execute_create_filter()).grid(
            column=0, row=9, columnspan=2)

        fig, self.ax = plt.subplots()
        self.ax.figure.set_size_inches(2, 1.5)
        self.ax.tick_params(axis='both', labelsize=3)
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=10, columnspan=2)

    def execute_create_filter(self):
        m = int(self.filter_m_entry.get())
        f0 = float(self.filter_f0_entry.get())
        fd = int(self.filter_fd_entry.get())
        window = None
        if self.window_var.get() == "Okno Hamminga":
            window = signal_zad3.hamming_window
        if self.type_var.get() == "dolnoprzepustowy":
            self.t_values, self.y_values = signal_zad3.get_low_pass_filter(m, f0, fd, window)
        elif self.type_var.get() == "górnoprzepustowy":
            self.t_values, self.y_values = signal_zad3.get_high_pass_filter(m, f0, fd, window)
        self.show_plot("Filtr", self.t_values, self.y_values)

    def show_plot(self, title: str, t_values, y_values, clear: bool = True):
        if clear:
            self.ax.clear()
            self.canvas.draw()
        self.ax.set_title(title, fontsize=6)
        self.ax.scatter(t_values, y_values, s=0.5)
        self.canvas.draw()
