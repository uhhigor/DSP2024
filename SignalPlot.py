import matplotlib.pyplot as plt

import Signal


def menu():
    print("1. Wyświetl wykres sygnału")
    print("2. Operacje na sygnałach")
    print("3. Wyjście")
    choice = int(input("Wybór: "))
    if choice == 1:
        signal, samples, signal_type = create_signal()
        signal_parameters(signal, signal_type, samples)
        create_plot(*values_to_list(signal, samples), signal_type)
    elif choice == 2:
        signal_operations()
    elif choice == 3:
        exit()
    else:
        print("Niepoprawny wybór")
        menu()


def signal_operations():
    signal1, samples1, signal_type1 = create_signal()
    signal2, samples2, signal_type2 = create_signal()

    n_samples = samples1

    print("Wybierz operację na sygnałach:")
    print("1. Dodawanie")
    print("2. Odejmowanie")
    print("3. Mnożenie")
    print("4. Dzielenie")
    choice = int(input("Wybór: "))
    if choice == 1:
        addition_signal = lambda n: signal1(n) + signal2(n)
        result = [addition_signal(n) for n in range(n_samples)]
    elif choice == 2:
        subtraction_signal = lambda n: signal1(n) - signal2(n)
        result = [subtraction_signal(n) for n in range(n_samples)]
    elif choice == 3:
        multiplication_signal = lambda n: signal1(n) * signal2(n)
        result = [multiplication_signal(n) for n in range(n_samples)]
    elif choice == 4:
        division_signal = lambda n: signal1(n) / signal2(n) if signal2(n) != 0 else 0
        result = [division_signal(n) for n in range(n_samples)]
    else:
        print("Niepoprawny wybór")
        return

    time_samples = [signal1.t(n) for n in range(n_samples)]

    create_plot(time_samples, result)


def signal_parameters(signal: (), signal_type: int, samples: int):
    if signal_type in range(1, 10):
        print("Obliczone wartości sygnału ciągłego:")
        print(f"Wartość średnia sygnału: {signal.continuous_average_value(signal)}")
        print(f"Wartość średnia bezwzględna: {signal.continuous_average_value_absolute(signal)}")
        print(f"Moc średnia sygnału: {signal.continuous_average_power(signal)}")
        print(f"Wariancja sygnału: {signal.continuous_variance(signal)}")
        print(f"Wartość skuteczna: {signal.continuous_effective_value(signal)}")
    else:
        print("Obliczone wartości sygnału dyskretnego:")
        print(f"Wartość średnia sygnału: {signal.discrete_average_value(signal, samples)}")
        print(f"Wartość średnia bezwzględna: {signal.discrete_average_value_absolute(signal, samples)}")
        print(f"Moc średnia sygnału: {signal.discrete_average_power(signal, samples)}")
        print(f"Wariancja sygnału: {signal.discrete_variance(signal, samples)}")
        print(f"Wartość skuteczna: {signal.discrete_effective_value(signal, samples)}")


def create_plot(t_values, y_values, signal_type=None):
    plt.subplot(2, 1, 1)
    if signal_type == 10 or signal_type == 11:
        plt.scatter(t_values, y_values)
    else:
        plt.plot(t_values, y_values)

    plt.subplot(2, 1, 2)
    bins = int(input("Histogram: Liczba przedzialów: "))
    plt.hist(y_values, bins=bins, edgecolor='black')
    plt.show()


def values_to_list(signal, samples):
    t_values = []
    y_values = []
    for n in range(0, samples):
        t_values.append(signal.t(n))
        y_values.append(signal(n))

    return t_values, y_values


def create_signal():
    print("Wybierz sygnał:")
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
    f = int(input("Częstotliwość próbkowania f: "))
    s = int(input("Liczba próbek n: "))
    A = float(input("Amplituda sygnału A: "))
    t1, d, T, kw, ts, ns, p = 0, 0, 0, 0, 0, 0, 0
    signal = None

    if signal_type != 10:
        t1 = float(input("Czas początkowy t1: "))
        d = float(input("Czas trwania sygnału d: "))
        signal = getattr(Signal, f"S{signal_type}")(A, t1, d, 0, f)
    if signal_type > 2 and signal_type not in range(9, 12):
        T = float(input("Okres podstawowy T: "))
        signal = getattr(Signal, f"S{signal_type}")(A, t1, d, T, f)
    if signal_type in range(6, 9):
        kw = float(input("Współczynnik kw: "))
        signal = getattr(Signal, f"S{signal_type}")(A, t1, d, T, f, kw)
    if signal_type == 9:
        ts = float(input("Czas skoku ts: "))
        signal = getattr(Signal, f"S{signal_type}")(A, t1, d, 0, f, ts)
    if signal_type == 10:
        ns = float(input("Numer próbki skoku ns: "))
        signal = getattr(Signal, f"S{signal_type}")(A, 0, 0, 0, f, ns)
    if signal_type == 11:
        p = float(input("Prawdopodobieństwo p: "))
        signal = getattr(Signal, f"S{signal_type}")(A, t1, d, 0, f, p)

    samples = s

    return signal, samples, signal_type


menu()
