from matplotlib import pyplot as plt

from api import analog_signal
from api.signal_conversion import uniform_sampling

sig = analog_signal.S3(1, 0, 10, 1)

t, samples = uniform_sampling(sig, 100, 5, 15)

plt.scatter(t, samples)
plt.show()

