from tkinter import *
from tkinter import ttk

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
selected_signal.set(signals[0])
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

    if selected_signal.get() in ["Szum o rozkładzie jednostajnym", "Szum gaussowski"]:
        t1_label.grid(column=0, row=2)
        t1_entry.grid(column=1, row=2)
        d_label.grid(column=0, row=3)
        d_entry.grid(column=1, row=3)
    elif selected_signal.get() in ["Sygnał sinusoidalny", "Sygnał sinusoidalny wyprostowany jednopołówkowo",
                                   "Sygnał sinusoidalny wyprostowany dwupołówkowo"]:
        t1_label.grid(column=0, row=2)
        t1_entry.grid(column=1, row=2)
        d_label.grid(column=0, row=3)
        d_entry.grid(column=1, row=3)
        T_label.grid(column=0, row=4)
        T_entry.grid(column=1, row=4)
    elif selected_signal.get() in ["Sygnał prostokątny", "Sygnał prostokątny symetryczny", "Sygnał trójkątny"]:
        t1_label.grid(column=0, row=2)
        t1_entry.grid(column=1, row=2)
        d_label.grid(column=0, row=3)
        d_entry.grid(column=1, row=3)
        T_label.grid(column=0, row=4)
        T_entry.grid(column=1, row=4)
        kw_label.grid(column=0, row=5)
        kw_entry.grid(column=1, row=5)
    elif selected_signal.get() == "Skok jednostkowy":
        t1_label.grid(column=0, row=2)
        t1_entry.grid(column=1, row=2)
        d_label.grid(column=0, row=3)
        d_entry.grid(column=1, row=3)
        ts_label.grid(column=0, row=4)
        ts_entry.grid(column=1, row=4)
    elif selected_signal.get() == "Impuls jednostkowy":
        ns_label.grid(column=0, row=2)
        ns_entry.grid(column=1, row=2)
    elif selected_signal.get() == "Szum impulsowy":
        t1_label.grid(column=0, row=2)
        t1_entry.grid(column=1, row=2)
        d_label.grid(column=0, row=3)
        d_entry.grid(column=1, row=3)
        p_label.grid(column=0, row=4)
        p_entry.grid(column=1, row=4)
    param_frame.update_idletasks()


show_params()
selected_signal.trace("w", show_params)
root.mainloop()
