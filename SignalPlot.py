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
f = int(input("Częstotliwość próbkowania: "))
s = int(input("Podaj liczbe próbek: "))
t1, d, T, kw, ts, ns, p = 0, 0, 0, 0, 0, 0, 0
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

samples = s

if signal_type in range(1, 10):
    print("Obliczone wartości sygnału ciągłego:")
    print(f"Wartość średnia sygnału: {signal.continuous_average_value(signal, f)}")
    print(f"Wartość średnia bezwzględnae: {signal.continuous_average_value_absolute(signal, f)}")
    print(f"Moc średnia sygnału: {signal.continuous_average_power(signal, f)}")
    print(f"Wariancja sygnału: {signal.continuous_variance(signal, f)}")
    print(f"Wartość skuteczna: {signal.continuous_effective_value(signal, f)}")
else:
    print("Obliczone wartości sygnału dyskretnego:")
    print(f"Wartość średnia sygnału: {signal.discrete_average_value(signal, samples)}")
    print(f"Wartość średnia bezwzględna: {signal.discrete_average_value_absolute(signal, samples)}")
    print(f"Moc średnia sygnału: {signal.discrete_average_power(signal, samples)}")
    print(f"Wariancja sygnału: {signal.discrete_variance(signal, samples)}")
    print(f"Wartość skuteczna: {signal.discrete_effective_value(signal, samples)}")


t_values = []
y_values = []
for n in range(0, samples):
    t_values.append(signal.t(n))
    y_values.append(signal(n))

plt.subplot(2, 1, 1)
if isinstance(signal, Signal.S10) or isinstance(signal, Signal.S11):
    plt.scatter(t_values, y_values)
else:
    plt.plot(t_values, y_values)

plt.subplot(2, 1, 2)
print("Wprowadź liczbę przedzialów:")
bins = int(input("Liczba przedzialów: "))
plt.hist(y_values, bins=bins, edgecolor='black')
plt.show()
