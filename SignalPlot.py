import matplotlib.pyplot as plt

import Signal

print("Wybierz sygnał do wyrysowania:")
signals = {
    1: "Szum o rozkładzie jednostajnym",
    2: "Szum gaussowski",
    3: "Sygnał sinusoidalny",
    4: "Sygnał sinusoidalny wyprostowany jednopołówkowo",
    5: "Sygnał sinusoidalny wyprostowany dwupołówkowo",
    6: "Sygnał prostokątny",
    7: "Sygnał prostokątny symetryczny",
    8: "Sygnał trójkątny",
    9: "Skok jednostkowy",
    10: "Impuls jednostkowy",
    11: "Szum impulsowy"
}
for key, value in signals.items():
    print(f"{key}. {value}")

signal_type = int(input("Wybór: "))

print("Wprowadz parametry sygnału")
A = float(input("A: "))
t1, d, T, f, kw, ts, ns, p = 0, 0, 0, 100, 0, 0, 0, 0
signal = None

if signal_type != 10:
    t1 = float(input("t1: "))
    d = float(input("d: "))
    signal = getattr(Signal, f"S{signal_type}")(A, t1, d, 0, f)
if signal_type > 2 and signal_type not in range(9, 12):
    T = float(input("T: "))
    signal = getattr(Signal, f"S{signal_type}")(A, t1, d, T, f)
if signal_type in range(6, 9):
    kw = float(input("kw: "))
    signal = getattr(Signal, f"S{signal_type}")(A, t1, d, T, f, kw)
if signal_type == 9:
    ts = float(input("ts: "))
    signal = getattr(Signal, f"S{signal_type}")(A, t1, d, 0, f, ts)
if signal_type == 10:
    ns = float(input("ns: "))
    signal = getattr(Signal, f"S{signal_type}")(A, 0, 0, 0, f, ns)
if signal_type == 11:
    p = float(input("p: "))
    signal = getattr(Signal, f"S{signal_type}")(A, t1, d, 0, f, p)


# 1000 próbek, 10 sekund, 100 próbek na sekundę (100 Hz)
# Amplituda 10, czas początkowy 0, czas trwania 10, okres podstawowy 5
t_values = []
y_values = []
samples = 1000

for n in range(0, samples):
    t_values.append(signal.t(n))
    y_values.append(signal(n))

if isinstance(signal, Signal.S10) or isinstance(signal, Signal.S11):
    plt.scatter(t_values, y_values)
else:
    plt.plot(t_values, y_values)
plt.show()
