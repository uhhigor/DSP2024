from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import Signal

root = Tk()
root.title("CPS - Projekt 1")
root.geometry("1000x800")
notebook = ttk.Notebook(root, padding=10)
notebook.pack(fill='both', expand=True)

page1 = ttk.Frame(notebook, padding=10)
notebook.add(page1, text="Generowanie sygnału")

ttk.Button(page1, text="Quit", command=root.destroy).grid(column=1, row=3)

param_frame = ttk.Frame(page1, padding=10)
param_frame.grid(column=0, row=2, columnspan=2)

# SIGNAL INFO FRAME

signal_info_frame = ttk.Frame(page1, padding=10)
signal_info_frame.grid(column=4, row=0, columnspan=2, rowspan=4)

avg_label = ttk.Label(signal_info_frame, text="Wartość średnia sygnału: ")
avg_label.grid(column=0, row=0)
avg_label_value = ttk.Label(signal_info_frame, text="")
avg_label_value.grid(column=1, row=0)

avg_abs_label = ttk.Label(signal_info_frame, text="Wartość średnia bezwzględna sygnału: ")
avg_abs_label.grid(column=0, row=1)
avg_abs_label_value = ttk.Label(signal_info_frame, text="")
avg_abs_label_value.grid(column=1, row=1)

avg_power_label = ttk.Label(signal_info_frame, text="Moc średnia sygnału: ")
avg_power_label.grid(column=0, row=2)
avg_power_label_value = ttk.Label(signal_info_frame, text="")
avg_power_label_value.grid(column=1, row=2)

variance_label = ttk.Label(signal_info_frame, text="Wariancja sygnału: ")
variance_label.grid(column=0, row=3)
variance_label_value = ttk.Label(signal_info_frame, text="")
variance_label_value.grid(column=1, row=3)

effective_label = ttk.Label(signal_info_frame, text="Wartość skuteczna sygnału: ")
effective_label.grid(column=0, row=4)
effective_label_value = ttk.Label(signal_info_frame, text="")
effective_label_value.grid(column=1, row=4)

# SIGNAL INFO FRAME END


ttk.Label(page1, text="Wybierz sygnał:").grid(column=0, row=1)
signal_map = {
    "None": None,
    "Szum o rozkładzie jednostajnym": Signal.S1,
    "Szum gaussowski": Signal.S2,
    "Sygnał sinusoidalny": Signal.S3,
    "Sygnał sinusoidalny wyprostowany jednopołówkowo": Signal.S4,
    "Sygnał sinusoidalny wyprostowany dwupołówkowo": Signal.S5,
    "Sygnał prostokątny": Signal.S6,
    "Sygnał prostokątny symetryczny": Signal.S7,
    "Sygnał trójkątny": Signal.S8,
    "Skok jednostkowy": Signal.S9,
    "Impuls jednostkowy": Signal.S10,
    "Szum impulsowy": Signal.S11
}
signals = list(signal_map.keys())
selected_signal = StringVar()
dropdown_signal = ttk.OptionMenu(page1, selected_signal, *signals)
dropdown_signal.config(width=30)
dropdown_signal.grid(column=1, row=1)
selected_signal.set("Szum o rozkładzie jednostajnym")

new_page = ttk.Frame(notebook, padding=10)
notebook.add(new_page, text="Operacje na sygnałach")

ttk.Label(new_page, text="Wybierz sygnał 1:").grid(column=0, row=0)
selected_signal1 = StringVar()
dropdown_signal = ttk.OptionMenu(new_page, selected_signal1, *signals)
dropdown_signal.config(width=30)
dropdown_signal.grid(column=1, row=0)
selected_signal1.set("Szum o rozkładzie jednostajnym")

param_frame1 = ttk.Frame(new_page, padding=10)
param_frame1.grid(column=0, row=2, columnspan=2)

selected_signal2 = StringVar()
dropdown_signal = ttk.OptionMenu(new_page, selected_signal2, *signals)
dropdown_signal.config(width=30)
dropdown_signal.grid(column=3, row=0)
selected_signal2.set("Szum o rozkładzie jednostajnym")

ttk.Label(new_page, text="Wybierz operację:").grid(column=4, row=0)
operations = ["None", "+", "-", "*", "/"]
selected_operation = StringVar()
dropdown_operation = ttk.OptionMenu(new_page, selected_operation, *operations)
dropdown_operation.grid(column=5, row=0)
selected_operation.set("+")




def show_signal_info(signal: Signal, samples):
    if signal is None:
        return
    if signal is Signal.S10 or signal is Signal.S11:
        avg_label_value.config(text=str(round(signal.discrete_average_value(signal, samples), 3)))
        avg_abs_label_value.config(text=str(round(signal.discrete_average_value_absolute(signal, samples), 3)))
        avg_power_label_value.config(text=str(round(signal.discrete_average_power(signal, samples), 3)))
        variance_label_value.config(text=str(round(signal.discrete_variance(signal, samples), 3)))
        effective_label_value.config(text=str(round(signal.discrete_effective_value(signal, samples), 3)))
    else:
        avg_label_value.config(text=str(round(signal.continuous_average_value(signal), 3)))
        avg_abs_label_value.config(text=str(round(signal.continuous_average_value_absolute(signal), 3)))
        avg_power_label_value.config(text=str(round(signal.continuous_average_power(signal), 3)))
        variance_label_value.config(text=str(round(signal.continuous_variance(signal), 3)))
        effective_label_value.config(text=str(round(signal.continuous_effective_value(signal), 3)))





def save_to_file(signal, samples, t_values, y_values, filename):
    params = {
        'start_time': signal.t(0),
        'sampling_frequency': signal.f,
        'num_samples': samples
    }
    y_array = np.array(y_values, dtype=np.float64)
    print(y_array)

    with open(filename, 'wb') as file:
        file.write(np.array([params['start_time']], dtype=np.float64).tobytes())
        file.write(np.array([params['sampling_frequency']], dtype=np.float64).tobytes())
        file.write(np.array([params['num_samples']], dtype=np.int32).tobytes())
        file.write(y_array.tobytes())
    print("Zapisano do pliku")


def load_from_file(filename):
    with open(filename, 'rb') as file:
        start_time = np.frombuffer(file.read(8), dtype=np.float64)[0]
        sampling_frequency = np.frombuffer(file.read(8), dtype=np.float64)[0]
        num_samples = np.frombuffer(file.read(4), dtype=np.int32)[0]

        y_values = np.frombuffer(file.read(), dtype=np.float64)

    t_values = np.linspace(start_time, start_time + num_samples / sampling_frequency, num_samples, endpoint=False)

    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)

    ax1.plot(t_values, y_values)
    ax2.hist(y_values, 10, edgecolor='black')

    canvas = FigureCanvasTkAgg(fig, master=page1)
    canvas.draw()
    canvas.get_tk_widget().grid(column=0, row=4, columnspan=4)


ttk.Button(page1, text="Load from file", command=lambda: load_from_file('gui/signal_data.bin')).grid(column=2, row=3)

root.mainloop()
