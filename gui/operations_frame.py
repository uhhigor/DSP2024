from tkinter import ttk, StringVar, Toplevel

from matplotlib import pyplot as plt

from plot_creation_frame import PlotCreationFrame
from signal_info_frame import SignalInfoFrame


class OperationsFrame:
    def __init__(self, master, function_frame1: PlotCreationFrame, function_frame2: PlotCreationFrame):
        self.master = master
        self.function_frame1 = function_frame1
        self.function_frame2 = function_frame2
        self.frame = ttk.Frame(self.master, padding="10")
        self.windows = []

        self.selected_operation = StringVar()
        self.init_op_dropdown()

        ttk.Button(self.frame, text="Wykonaj operację", command=self.execute_operation).grid(column=1, row=0)

    def init_op_dropdown(self):
        operations = ["None", "+", "-", "*", "/"]
        dropdown_operation = ttk.OptionMenu(self.frame, self.selected_operation, *operations)
        dropdown_operation.grid(column=5, row=0)
        self.selected_operation.set("+")

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

    def execute_operation(self):
        self.close_other()
        values1 = self.function_frame1.current.samples
        values2 = self.function_frame2.current.samples
        t_values = self.function_frame1.current.time

        if len(values1) != len(values2):
            print("Sygnały muszą mieć taką samą liczbę próbek")
            return

        operation = self.selected_operation.get()
        result = []
        for i in range(len(values1)):
            if operation == "+":
                result.append(values1[i] + values2[i])
            elif operation == "-":
                result.append(values1[i] - values2[i])
            elif operation == "*":
                result.append(values1[i] * values2[i])
            elif operation == "/":
                result.append(values1[i] / values2[i] if values2[i] != 0 else 0)
            else:
                print("Niepoprawna operacja")
                return

        fig = plt.figure()
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)

        ax1.plot(t_values, result)
        ax2.hist(result, 10, edgecolor='black')
        self.show_info(result, fig, self.function_frame1.current.sampling_rate, self.function_frame1.current.start_time, len(result), "Wynik operacji")
