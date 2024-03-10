import matplotlib.pyplot as plt

import Signal

# 1000 próbek, 10 sekund, 100 próbek na sekundę (100 Hz)
# Amplituda 10, czas początkowy 0, czas trwania 10, okres podstawowy 5
t_values = []
y_values = []
samples = 1000
signal: Signal.ContinuousSignal = Signal.S9(10, 0, 10, 5, 100)
for n in range(0, samples):
    t_values.append(signal.t(n))
    y_values.append(signal(n))

plt.plot(t_values, y_values)
plt.show()

