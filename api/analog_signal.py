import math
import random
import numpy as np


class AnalogSignal:
    def __init__(self):
        pass

    def __call__(self, t):
        pass

    def get_simulated_values(self, t1: float, t2: float, sampling_freq: int = 10000) -> tuple:
        n_samples = int(sampling_freq * abs(t2 - t1))
        t_values = np.linspace(t1, t2, n_samples)
        y_values = [self(t) for t in t_values]
        return y_values, t_values


class ContinuousAnalogSignal(AnalogSignal):
    def __init__(self, amplitude: float, t1: float, duration: float, period: float):
        super().__init__()
        self.amplitude = amplitude  # amplituda - wartość maksymalna
        self.t1 = t1  # czas początkowy, poniżej którego sygnał jest równy 0
        self.duration = duration  # czas trwania sygnału
        self.period = period  # okres podstawowy
        self.t2 = t1 + duration  # czas końcowy, powyżej którego sygnał jest równy 0

    def __call__(self, t) -> float:  # t - czas
        pass


class DiscreteAnalogSignal(AnalogSignal):
    def __init__(self, amplitude: float):
        super().__init__()
        self.amplitude = amplitude

    def __call__(self, n) -> float:  # n - numer próbki
        pass


class S1(ContinuousAnalogSignal):
    def __init__(self, amplitude, t1, duration, period):
        super().__init__(amplitude, t1, duration, period)

    def __call__(self, t) -> float:
        if t < self.t1:
            return 0
        elif t > self.t1 + self.duration:
            return 0
        else:
            return random.uniform(-self.amplitude, self.amplitude)


class S2(ContinuousAnalogSignal):
    def __init__(self, amplitude, t1, duration, period):
        super().__init__(amplitude, t1, duration, period)

    def noise(self, x):
        return math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)

    def __call__(self, t):
        if t < self.t1:
            return 0
        elif t > self.t1 + self.duration:
            return 0
        else:
            r = random.uniform(-self.amplitude, self.amplitude)
            return r + self.noise(t)


class S3(ContinuousAnalogSignal):
    def __init__(self, amplitude, t1, duration, period):
        super().__init__(amplitude, t1, duration, period)

    def __call__(self, t):
        if t < self.t1:
            return 0
        elif t > self.t1 + self.duration:
            return 0
        else:
            return self.amplitude * math.sin(2.0 * math.pi * (t - self.t1) / self.period)


class S4(ContinuousAnalogSignal):
    def __init__(self, amplitude, t1, duration, period):
        super().__init__(amplitude, t1, duration, period)

    def __call__(self, t):
        if t < self.t1:
            return 0
        elif t > self.t1 + self.duration:
            return 0
        else:
            return (self.amplitude / 2) * (math.sin(2.0 * math.pi * (t - self.t1) / self.period) + math.fabs(
                math.sin(2.0 * math.pi * (t - self.t1) / self.period)))


class S5(ContinuousAnalogSignal):
    def __init__(self, amplitude, t1, duration, period):
        super().__init__(amplitude, t1, duration, period)

    def __call__(self, t):
        if t < self.t1:
            return 0
        elif t > self.t1 + self.duration:
            return 0
        else:
            return self.amplitude * math.fabs(math.sin(2.0 * math.pi * (t - self.t1) / self.period))


# kw - stosunek czasu trwania wartości maksymalnej do okresu podstawowego (0 < kw < 1)
class S6(ContinuousAnalogSignal):
    def __init__(self, amplitude, t1, duration, period, kw=0.5):
        super().__init__(amplitude, t1, duration, period)
        self.kw = kw

    def __call__(self, t):
        if t < self.t1:
            return 0
        elif t > self.t1 + self.duration:
            return 0
        else:
            if t % self.period < self.kw * self.period:
                return self.amplitude
            else:
                return 0


# kw - stosunek czasu trwania wartości maksymalnej do okresu podstawowego (0 < kw < 1)
class S7(ContinuousAnalogSignal):
    def __init__(self, amplitude, t1, duration, period, kw=0.5):
        super().__init__(amplitude, t1, duration, period)
        self.kw = kw

    def __call__(self, t):
        if t < self.t1:
            return 0
        elif t > self.t1 + self.duration:
            return 0
        else:
            if t % self.period < self.kw * self.period:
                return self.amplitude
            else:
                return -self.amplitude


# kw - stosunek czasu trwania zbocza narastającego do okresu podstawowego (0 < kw < 1)
class S8(ContinuousAnalogSignal):
    def __init__(self, amplitude, t1, duration, period, kw=0.5):
        super().__init__(amplitude, t1, duration, period)
        self.kw = kw

    def __call__(self, t):
        if t < self.t1:
            return 0
        elif t > self.t1 + self.duration:
            return 0
        else:
            k = (t % self.period) / self.period
            if k < self.kw:
                return self.amplitude * k
            else:
                return self.amplitude * (1 - k)


class S9(ContinuousAnalogSignal):

    def __init__(self, amplitude, t1, duration, period, ts):
        super().__init__(amplitude, t1, duration, period)
        self.ts = ts

    def __call__(self, t):
        if t < self.t1:
            return 0
        elif t > self.t1 + self.duration:
            return 0
        else:
            if t > self.ts:
                return self.amplitude
            elif t == self.ts:
                return self.amplitude / 2
            elif t < self.ts:
                return 0


class S10(DiscreteAnalogSignal):
    def __init__(self, amplitude, ns):
        super().__init__(amplitude)
        self.amplitude = amplitude
        self.ns = ns

    def __call__(self, n):
        if n == self.ns:
            return self.amplitude
        else:
            return 0


class S11(DiscreteAnalogSignal):
    def __init__(self, amplitude, p=0.5):
        super().__init__(amplitude)
        self.amplitude = amplitude
        self.p = p

    def __call__(self, n):
        rand = random.random()
        if rand >= self.p:
            return 0
        else:
            return self.amplitude
