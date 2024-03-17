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

new_page = ttk.Frame(notebook, padding=10)
notebook.add(new_page, text="Operacje na sygnałach")

ttk.Label(new_page, text="Wybierz sygnał 1:").grid(column=0, row=0)
selected_signal1 = StringVar()
dropdown_signal = ttk.OptionMenu(new_page, selected_signal1, *signals)
dropdown_signal.config(width=30)
dropdown_signal.grid(column=1, row=0)

param_frame1 = ttk.Frame(new_page, padding=10)
param_frame1.grid(column=0, row=2, columnspan=2)


selected_signal2 = StringVar()
dropdown_signal = ttk.OptionMenu(new_page, selected_signal2, *signals)
dropdown_signal.config(width=30)
dropdown_signal.grid(column=3, row=0)


ttk.Label(new_page, text="Wybierz operację:").grid(column=4, row=0)
operations = ["Dodawanie", "Odejmowanie", "Mnożenie", "Dzielenie"]
selected_operation = StringVar()
dropdown_operation = ttk.OptionMenu(new_page, selected_operation, *operations)
dropdown_operation.config(width=30)
dropdown_operation.grid(column=5, row=0)


def only_numbers(char: chr):
    return char.isdigit() or char == "."


f_label = ttk.Label(param_frame, text="Częstotliwość próbkowania f: ")
f_entry = ttk.Entry(param_frame, validate="key", validatecommand=(root.register(only_numbers), "%S"))

A_label = ttk.Label(param_frame, text="Amplituda sygnału A: ")
A_entry = ttk.Entry(param_frame, validate="key", validatecommand=(root.register(only_numbers), "%S"))

t1_label = ttk.Label(param_frame, text="Czas początkowy t1: ")
t1_entry = ttk.Entry(param_frame, validate="key", validatecommand=(root.register(only_numbers), "%S"))

d_label = ttk.Label(param_frame, text="Czas trwania sygnału d: ")
d_entry = ttk.Entry(param_frame, validate="key", validatecommand=(root.register(only_numbers), "%S"))

T_label = ttk.Label(param_frame, text="Okres podstawowy T: ")
T_entry = ttk.Entry(param_frame, validate="key", validatecommand=(root.register(only_numbers), "%S"))

kw_label = ttk.Label(param_frame, text="Współczynnik kw: ")
kw_entry = ttk.Entry(param_frame, validate="key", validatecommand=(root.register(only_numbers), "%S"))

ts_label = ttk.Label(param_frame, text="Czas skoku ts: ")
ts_entry = ttk.Entry(param_frame, validate="key", validatecommand=(root.register(only_numbers), "%S"))

ns_label = ttk.Label(param_frame, text="Numer próbki skoku ns: ")
ns_entry = ttk.Entry(param_frame, validate="key", validatecommand=(root.register(only_numbers), "%S"))

p_label = ttk.Label(param_frame, text="Prawdopodobieństwo p: ")
p_entry = ttk.Entry(param_frame, validate="key", validatecommand=(root.register(only_numbers), "%S"))

n1_label = ttk.Label(param_frame, text="Numer pierwszej próbki: ")
n1_entry = ttk.Entry(param_frame, validate="key", validatecommand=(root.register(only_numbers), "%S"))

h_label = ttk.Label(param_frame, text="Liczba przedziałów histogramu: ")
h_entry = ttk.Entry(param_frame, validate="key", validatecommand=(root.register(only_numbers), "%S"))


def show_params(*args):
    for widget in param_frame.winfo_children():
        widget.grid_forget()
    f_label.grid(column=0, row=0)
    f_entry.grid(column=1, row=0)
    A_label.grid(column=0, row=2)
    A_entry.grid(column=1, row=2)
    t1_label.grid(column=0, row=3)
    t1_entry.grid(column=1, row=3)
    d_label.grid(column=0, row=4)
    d_entry.grid(column=1, row=4)
    T_label.grid(column=0, row=5)
    T_entry.grid(column=1, row=5)

    h_entry.grid(column=1, row=7)
    h_label.grid(column=0, row=7)

    if selected_signal.get() in ["Sygnał prostokątny", "Sygnał prostokątny symetryczny", "Sygnał trójkątny"]:
        kw_label.grid(column=0, row=6)
        kw_entry.grid(column=1, row=6)
    elif selected_signal.get() == "Skok jednostkowy":
        ts_label.grid(column=0, row=6)
        ts_entry.grid(column=1, row=6)
    elif selected_signal.get() == "Impuls jednostkowy":
        ns_label.grid(column=0, row=6)
        ns_entry.grid(column=1, row=6)
    elif selected_signal.get() == "Szum impulsowy":
        p_label.grid(column=0, row=6)
        p_entry.grid(column=1, row=6)
    param_frame.update_idletasks()


def create_signal():
    signal = signal_map.get(selected_signal.get())
    if signal in [Signal.S1, Signal.S2]:
        return signal(float(A_entry.get()), float(t1_entry.get()), float(d_entry.get()), float(T_entry.get()),
                      int(f_entry.get()))
    elif signal in [Signal.S3, Signal.S4, Signal.S5]:
        return signal(float(A_entry.get()), float(t1_entry.get()), float(d_entry.get()), float(T_entry.get()),
                      int(f_entry.get()))
    elif signal in [Signal.S6, Signal.S7, Signal.S8]:
        return signal(float(A_entry.get()), float(t1_entry.get()), float(d_entry.get()), float(T_entry.get()),
                      int(f_entry.get()), float(kw_entry.get()))
    elif signal == Signal.S9:
        return signal(float(A_entry.get()), float(t1_entry.get()), float(d_entry.get()), float(T_entry.get()),
                      int(f_entry.get()), float(ts_entry.get()))
    elif signal == Signal.S10:
        return signal(float(A_entry.get()), float(t1_entry.get()), float(d_entry.get()), float(T_entry.get()),
                      int(f_entry.get()), float(ns_entry.get()))
    elif signal == Signal.S11:
        return signal(float(A_entry.get()), float(t1_entry.get()), float(d_entry.get()), float(T_entry.get()),
                      int(f_entry.get()), float(p_entry.get()))
    else:
        return None


def create_values(signal, samples):
    t_values = []
    y_values = []
    for n in range(0, samples):
        t_values.append(signal.t(n))
        y_values.append(signal(n))
    return t_values, y_values


def plot_signal(signal: Signal, samples):
    t_values, y_values = create_values(signal, samples)
    save_to_file(signal, samples, t_values, y_values, 'signal_data.bin')
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)

    if signal is Signal.S10 or signal is Signal.S11:
        ax1.scatter(t_values, y_values)
    else:
        ax1.plot(t_values, y_values)

    ax2.hist(y_values, bins=int(h_entry.get()), edgecolor='black')
    return fig


def show_plot(signal: Signal, samples):
    fig = plot_signal(signal, samples)
    canvas = FigureCanvasTkAgg(fig, master=page1)
    canvas.draw()
    canvas.get_tk_widget().grid(column=0, row=4, columnspan=4)


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


def generate_btn():
    samples = int(f_entry.get()) * int(d_entry.get())
    signal = create_signal()
    show_signal_info(signal, samples)
    show_plot(signal, samples)


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


ttk.Button(page1, text="Generate", command=generate_btn).grid(column=0, row=3)
ttk.Button(page1, text="Load from file", command=lambda: load_from_file('signal_data.bin')).grid(column=1, row=3)


show_params()
selected_signal.trace("w", show_params)
root.mainloop()




