import math
import random
class S1:
    def __init__(self, A, t1, d):
        self.A = math.fabs(A)
        if t1 < 0:
            self.t1 = 0
        else:
            self.t1 = t1
        self.d = d

    def x(self, t):
        if t < self.t1:
            return 0
        elif t > self.t1 + self.d:
            return 0
        else:
            return random.uniform(-self.A, self.A)


class S2(S1):
    def __init__(self, A, t1, d):
        super().__init__(A, t1, d)

    def noise(self, x):
        return math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)

    def x(self, t):
        if t < self.t1:
            return 0
        elif t > self.t1 + self.d:
            return 0
        else:
            r = random.uniform(-self.A, self.A)
            return r + self.noise(r)


class S3:
    def __init__(self, A, T, t1, d):
        self.A = math.fabs(A)
        self.T = T
        if t1 < 0:
            self.t1 = 0
        else:
            self.t1 = t1
        self.d = d

    def x(self, t):
        if t < self.t1:
            return 0
        elif t > self.t1 + self.d:
            return 0
        else:
            return self.A * math.sin(2.0 * math.pi * (t - self.t1) / self.T)


class S4(S3):
    def __init__(self, A, T, t1, d):
        super().__init__(A, T, t1, d)

    def x(self, t):
        if t < self.t1:
            return 0
        elif t > self.t1 + self.d:
            return 0
        else:
            return (self.A / 2) * (math.sin(2.0 * math.pi * (t - self.t1) / self.T) + math.fabs(
                math.sin(2.0 * math.pi * (t - self.t1) / self.T)))


class S5(S3):
    def __init__(self, A, T, t1, d):
        super().__init__(A, T, t1, d)

    def x(self, t):
        if t < self.t1:
            return 0
        elif t > self.t1 + self.d:
            return 0
        else:
            return self.A * math.fabs(math.sin(2.0 * math.pi * (t - self.t1) / self.T))


# ???
class S6:
    def __init__(self, A, T, t1, d, kw):
        self.A = math.fabs(A)
        self.T = T
        if t1 < 0:
            self.t1 = 0
        else:
            self.t1 = t1
        self.d = d
        self.kw = kw

        self.k = 1

    def x(self, t):
        if t < self.t1:
            return 0
        elif t > self.t1 + self.d:
            return 0
        else:
            if self.k * self.T + self.t1 <= t < self.kw * self.T + self.k * self.T + self.t1:
                self.k += 1
                return self.A
            elif self.kw * self.T - self.k * self.T + self.t1 <= t < self.T + self.k * self.T + self.t1:
                return 0


class S7(S6):
    def __init__(self, A, T, t1, d, kw):
        super().__init__(A, T, t1, d, kw)

    def x(self, t):
        result = super().x(t)
        if result == 0:
            return -result
        else:
            return result


class S8(S6):
    def __init__(self, A, T, t1, d, kw):
        super().__init__(A, T, t1, d, kw)

    def x(self, t):
        if t < self.t1:
            return 0
        elif t > self.t1 + self.d:
            return 0
        else:
            if self.k * self.T + self.t1 <= t < self.kw * self.T + self.k * self.T + self.t1:
                self.k += 1
                return (self.A * (self.T - self.k * self.T - self.t1)) / (self.kw * self.T)
            elif self.kw * self.T - self.k * self.T + self.t1 <= t < self.T + self.k * self.T + self.t1:
                return ((-self.A * (self.T - self.k * self.T - self.t1))
                        / (self.T * (1 - self.kw)) + self.A / (1 - self.kw))


class S9:
    def __init__(self, A, t1, d, ts):
        self.A = math.fabs(A)
        if t1 < 0:
            self.t1 = 0
        else:
            self.t1 = t1
        self.d = d
        self.ts = ts

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

