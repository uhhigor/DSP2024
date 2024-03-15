from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import Signal

root = Tk()
root.title("Sygnały")
main_frame = ttk.Frame(root, padding=10)
main_frame.grid()
ttk.Button(main_frame, text="Quit", command=root.destroy).grid(column=1, row=4)

param_frame = ttk.Frame(main_frame, padding=10)
param_frame.grid(column=0, row=2, columnspan=2)

ttk.Label(main_frame, text="Wybierz sygnał:").grid(column=0, row=1)
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
dropdown_signal = ttk.OptionMenu(main_frame, selected_signal, *signals)
dropdown_signal.config(width=30)
dropdown_signal.grid(column=1, row=1)

f_label = ttk.Label(param_frame, text="Częstotliwość próbkowania f: ")
f_entry = ttk.Entry(param_frame)

s_label = ttk.Label(param_frame, text="Liczba próbek n: ")
s_entry = ttk.Entry(param_frame)

A_label = ttk.Label(param_frame, text="Amplituda sygnału A: ")
A_entry = ttk.Entry(param_frame)

t1_label = ttk.Label(param_frame, text="Czas początkowy t1: ")
t1_entry = ttk.Entry(param_frame)

d_label = ttk.Label(param_frame, text="Czas trwania sygnału d: ")
d_entry = ttk.Entry(param_frame)

T_label = ttk.Label(param_frame, text="Okres podstawowy T: ")
T_entry = ttk.Entry(param_frame)

kw_label = ttk.Label(param_frame, text="Współczynnik kw: ")
kw_entry = ttk.Entry(param_frame)

ts_label = ttk.Label(param_frame, text="Czas skoku ts: ")
ts_entry = ttk.Entry(param_frame)

ns_label = ttk.Label(param_frame, text="Numer próbki skoku ns: ")
ns_entry = ttk.Entry(param_frame)

p_label = ttk.Label(param_frame, text="Prawdopodobieństwo p: ")
p_entry = ttk.Entry(param_frame)

n1_label = ttk.Label(param_frame, text="Numer pierwszej próbki: ")
n1_entry = ttk.Entry(param_frame)


def show_params(*args):
    for widget in param_frame.winfo_children():
        widget.grid_forget()
    f_label.grid(column=0, row=0)
    f_entry.grid(column=1, row=0)
    s_label.grid(column=0, row=1)
    s_entry.grid(column=1, row=1)
    A_label.grid(column=0, row=2)
    A_entry.grid(column=1, row=2)
    t1_label.grid(column=0, row=3)
    t1_entry.grid(column=1, row=3)
    d_label.grid(column=0, row=4)
    d_entry.grid(column=1, row=4)
    T_label.grid(column=0, row=5)
    T_entry.grid(column=1, row=5)

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
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)

    if signal is Signal.S10 or signal is Signal.S11:
        ax1.scatter(t_values, y_values)
    else:
        ax1.plot(t_values, y_values)

    # plt.subplot(2, 1, 2)
    # bins = int(input("Histogram: Liczba przedzialów: "))
    ax2.hist(y_values, bins=5, edgecolor='black')
    return fig


def show_plot():
    signal = create_signal()
    samples = int(s_entry.get())
    fig = plot_signal(signal, samples)
    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(column=0, row=3, columnspan=4)


ttk.Button(main_frame, text="Show plot", command=show_plot).grid(column=0, row=4)

show_params()
selected_signal.trace("w", show_params)
root.mainloop()
