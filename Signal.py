import math
import random


# próbkowanie: 1hz = co 1 sekundę
class ContinuousSignal:
    def __init__(self, A: float, t1: float, d: float, T: float, f: float = 1):
        self.A = A  # amplituda - wartość maksymalna
        self.t1 = t1  # czas początkowy, poniżej którego sygnał jest równy 0
        self.d = d  # czas trwania sygnału
        self.T = T  # okres podstawowy
        self.f = f  # częstotliwość próbkowania
        self.t2 = t1 + d  # czas końcowy, powyżej którego sygnał jest równy 0

    def __call__(self, n):  # n - numer próbki
        pass

    def t(self, n):  # n - numer próbki, zwraca czas próbki
        return n / self.f

    def average_value(self, x: ()):
        sumxt = 0
        n = 0
        while self.t(n) < self.t2:
            sumxt += x(self.t(n))
            n += 1
        return sumxt / (self.t2 - self.t1)

    def average_value_absolute(self, x: ()):
        sumxt = 0
        n = 0
        while self.t(n) < self.t2:
            sumxt += math.fabs(x(self.t(n)))
            n += 1
        return sumxt / (self.t2 - self.t1)

    def average_power(self, x: ()):
        sumxt = 0
        n = 0
        while self.t(n) < self.t2:
            sumxt += x(self.t(n)) ** 2
            n += 1
        return sumxt / (self.t2 - self.t1)

    def variance(self, x: ()):
        sumxt = 0
        n = 0
        while self.t(n) < self.t2:
            sumxt += (x(self.t(n)) - self.average_value(x)) ** 2
            n += 1
        return sumxt / (self.t2 - self.t1)

    def effective_value(self, x: ()):
        return math.sqrt(self.average_power(x))


class S1(ContinuousSignal):
    def __init__(self, A, t1, d, T, f=1):
        super().__init__(A, t1, d, T, f)

    def __call__(self, n):  # n - numer próbki
        t_n = super().t(n)
        if t_n < self.t1:
            return 0
        elif t_n > self.t1 + self.d:
            return 0
        else:
            return random.uniform(-self.A, self.A)


class S2(ContinuousSignal):
    def __init__(self, A, t1, d, T, f=1):
        super().__init__(A, t1, d, T, f)

    def noise(self, x):
        return math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)

    def __call__(self, n):  # n - numer próbki
        t_n = super().t(n)
        if t_n < self.t1:
            return 0
        elif t_n > self.t1 + self.d:
            return 0
        else:
            r = random.uniform(-self.A, self.A)
            return r + self.noise(t_n)


class S3(ContinuousSignal):
    def __init__(self, A, t1, d, T, f=1):
        super().__init__(A, t1, d, T, f)

    def __call__(self, n):  # n - numer próbki
        t_n = super().t(n)
        if t_n < self.t1:
            return 0
        elif t_n > self.t1 + self.d:
            return 0
        else:
            return self.A * math.sin(2.0 * math.pi * (t_n - self.t1) / self.T)


class S4(ContinuousSignal):
    def __init__(self, A, t1, d, T, f=1):
        super().__init__(A, t1, d, T, f)

    def __call__(self, n):  # n - numer próbki
        t_n = super().t(n)
        if t_n < self.t1:
            return 0
        elif t_n > self.t1 + self.d:
            return 0
        else:
            return (self.A / 2) * (math.sin(2.0 * math.pi * (t_n - self.t1) / self.T) + math.fabs(
                math.sin(2.0 * math.pi * (t_n - self.t1) / self.T)))


class S5(ContinuousSignal):
    def __init__(self, A, t1, d, T, f=1):
        super().__init__(A, t1, d, T, f)

    def __call__(self, n):  # n - numer próbki
        t_n = super().t(n)
        if t_n < self.t1:
            return 0
        elif t_n > self.t1 + self.d:
            return 0
        else:
            return self.A * math.fabs(math.sin(2.0 * math.pi * (t_n - self.t1) / self.T))


# ???
class S6(ContinuousSignal):

    def __init__(self, A, t1, d, T, f=1):
        super().__init__(A, t1, d, T, f)
        self.kw = A / T

    def __call__(self, n):  # n - numer próbki
        t_n = super().t(n)
        k = t_n // self.T
        if t_n < self.t1:
            return 0
        elif t_n > self.t1 + self.d:
            return 0
        else:
            if k * self.T + self.t1 <= t_n < self.kw * self.T + k * self.T + self.t1:
                return self.A
            elif self.kw * self.T - k * self.T + self.t1 <= t_n < self.T + k * self.T + self.t1:
                return 0


# ???
class S7(ContinuousSignal):
    pass


# ???
class S8(ContinuousSignal):
    pass


class S9(ContinuousSignal):
    def __init__(self, A, t1, d, T, f=1, ts=0):
        super().__init__(A, t1, d, T, f)
        self.ts = ts

    def __call__(self, n):  # n - numer próbki
        t_n = super().t(n)
        if t_n < self.t1:
            return 0
        elif t_n > self.t1 + self.d:
            return 0
        else:
            if t_n > self.ts:
                return self.A
            elif t_n == self.ts:
                return self.A / 2
            elif t_n < self.ts:
                return 0

    def x(self, t):
        if t < self.t1:
            return 0
        elif t > self.t1 + self.d:
            return 0
        else:
            if t > self.ts:
                return self.A
            elif t == self.ts:
                return self.A / 2
            elif t < self.ts:
                return 0
