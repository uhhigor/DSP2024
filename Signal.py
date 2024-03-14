import math
import random
# próbkowanie: 1hz = co 1 sekundę


class Signal:
    def __init__(self, A: float, t1: float, d: float, T: float = 0, f: float = 1):
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

    def continuous_average_value(self, x):
        sumxt = 0
        interval_width = (self.t2 - self.t1) / self.f
        n = 0
        while self.t(n) < self.t2:
            sumxt += x(n) * interval_width
            n += 1

        return sumxt / (self.t2 - self.t1)

    def discrete_average_value(self, x, n):
        sumxt = 0
        i = 0
        if isinstance(x, S10):
            while i < n:
                sumxt += x(i)
                i += 1
        else:
            while self.t(i) < self.t2:
                sumxt += x(i)
                i += 1

        return sumxt / n

    def continuous_average_value_absolute(self, x):
        sumxt = 0
        interval_width = (self.t2 - self.t1) / self.f
        n = 0
        while self.t(n) < self.t2:
            sumxt += math.fabs(x(n)) * interval_width
            n += 1

        return sumxt / (self.t2 - self.t1)

    def discrete_average_value_absolute(self, x, n):
        sumxt = 0
        i = 0
        if isinstance(x, S10):
            while i < n:
                sumxt += math.fabs(x(i))
                i += 1
        else:
            while self.t(i) < self.t2:
                sumxt += math.fabs(x(i))
                i += 1

        return sumxt / n

    def continuous_average_power(self, x):
        sumxt = 0
        interval_width = (self.t2 - self.t1) / self.f
        n = 0
        while self.t(n) < self.t2:
            sumxt += x(n) ** 2 * interval_width
            n += 1

        return sumxt / (self.t2 - self.t1)

    def discrete_average_power(self, x, n):
        sumxt = 0
        i = 0
        if isinstance(x, S10):
            while i < n:
                sumxt += x(i) ** 2
                i += 1
        else:
            while self.t(i) < self.t2:
                sumxt += x(i) ** 2
                i += 1

        return sumxt / n

    def continuous_variance(self, x):
        avg_value = self.continuous_average_value(x)
        sumxt = 0
        interval_width = (self.t2 - self.t1) / self.f
        n = 0
        while self.t(n) < self.t2:
            sumxt += (x(n) - avg_value) ** 2 * interval_width
            n += 1

        return sumxt / (self.t2 - self.t1)

    def discrete_variance(self, x, n):
        avg_value = self.discrete_average_value(x, n)
        sumxt = 0
        i = 0
        if isinstance(x, S10):
            while i < n:
                sumxt += (x(i) - avg_value) ** 2
                i += 1
        else:
            while self.t(i) < self.t2:
                sumxt += (x(i) - avg_value) ** 2
                i += 1

        return sumxt / n

    def continuous_effective_value(self, x):
        return math.sqrt(self.continuous_average_power(x))

    def discrete_effective_value(self, x, n):
        return math.sqrt(self.discrete_average_power(x, n))


class S1(Signal):
    def __init__(self, A, t1, d, T, f):
        super().__init__(A, t1, d, T, f)

    def __call__(self, n):  # n - numer próbki
        t_n = super().t(n)
        if t_n < self.t1:
            return 0
        elif t_n > self.t1 + self.d:
            return 0
        else:
            return random.uniform(-self.A, self.A)


class S2(Signal):
    def __init__(self, A, t1, d, T, f):
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


class S3(Signal):
    def __init__(self, A, t1, d, T, f):
        super().__init__(A, t1, d, T, f)

    def __call__(self, n):  # n - numer próbki
        t_n = super().t(n)
        if t_n < self.t1:
            return 0
        elif t_n > self.t1 + self.d:
            return 0
        else:
            return self.A * math.sin(2.0 * math.pi * (t_n - self.t1) / self.T)


class S4(Signal):
    def __init__(self, A, t1, d, T, f):
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


class S5(Signal):
    def __init__(self, A, t1, d, T, f):
        super().__init__(A, t1, d, T, f)

    def __call__(self, n):  # n - numer próbki
        t_n = super().t(n)
        if t_n < self.t1:
            return 0
        elif t_n > self.t1 + self.d:
            return 0
        else:
            return self.A * math.fabs(math.sin(2.0 * math.pi * (t_n - self.t1) / self.T))


# kw - stosunek czasu trwania wartości maksymalnej do okresu podstawowego (0 < kw < 1)
class S6(Signal):

    def __init__(self, A, t1, d, T, f, kw=0.5):
        super().__init__(A, t1, d, T, f)
        self.kw = kw

    def __call__(self, n):  # n - numer próbki
        t_n = super().t(n)
        if t_n < self.t1:
            return 0
        elif t_n > self.t1 + self.d:
            return 0
        else:
            if t_n % self.T < self.kw * self.T:
                return self.A
            else:
                return 0


# kw - stosunek czasu trwania wartości maksymalnej do okresu podstawowego (0 < kw < 1)
class S7(Signal):
    def __init__(self, A, t1, d, T, f, kw=0.5):
        super().__init__(A, t1, d, T, f)
        self.kw = kw

    def __call__(self, n):  # n - numer próbki
        t_n = super().t(n)
        if t_n < self.t1:
            return 0
        elif t_n > self.t1 + self.d:
            return 0
        else:
            if t_n % self.T < self.kw * self.T:
                return self.A
            else:
                return -self.A


# kw - stosunek czasu trwania zbocza narastającego do okresu podstawowego (0 < kw < 1)
class S8(Signal):
    def __init__(self, A, t1, d, T, f, kw=0.5):
        super().__init__(A, t1, d, T, f)
        self.kw = kw

    def __call__(self, n):  # n - numer próbki
        t_n = super().t(n)
        if t_n < self.t1:
            return 0
        elif t_n > self.t1 + self.d:
            return 0
        else:
            k = (t_n % self.T) / self.T
            if k < self.kw:
                return self.A * k
            else:
                return self.A * (1 - k)


class S9(Signal):
    def __init__(self, A, t1, d, T, f, ts=0):
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


class S10(Signal):
    def __init__(self, A, t1, d, T, f, ns=0):
        super().__init__(A, t1, d, T, f)
        self.ns = ns

    def __call__(self, n):  # n - numer próbki
        t_n = super().t(n)
        if t_n == (self.ns / self.f):
            return self.A
        else:
            return 0


class S11(Signal):
    def __init__(self, A, t1, d, T, f, p=0.5):
        super().__init__(A, t1, d, T, f)
        self.p = p

    def __call__(self, n):  # n - numer próbki
        t_n = super().t(n)
        if t_n < self.t1:
            return 0
        elif t_n > self.t1 + self.d:
            return 0
        else:
            rand = random.random()
            if rand >= self.p:
                return 0
            else:
                return self.A
