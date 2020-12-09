import unittest
from counters import *
import random
import numpy as np

counterClasses = [Counter, MorrisCounter, MorrisAlpha, RedisCounter]

def within(value, expected, tolerance):
    return expected - tolerance <= value <= expected + tolerance

def run(counterClass, kwargs, times, N):
    res = []
    for _ in range(times):
        counter = counterClass(**kwargs)
        for _ in range(N):
            counter.update()
        res.append(counter.query())
    return np.array(res)

seed = 42

class TestStandardDeviation(unittest.TestCase):
    N = 10000
    times = 100

    def test_Counter_standard_deviation(self):
        vals = run(Counter, {}, self.times, self.N)
        within_25_percent = np.mean((self.N - self.N/4 <= vals) & (self.N + self.N/4 >= vals))
        print("\nFor Counter,", str(within_25_percent * 100)+"% of runs are within 25% on either side of", self.N, "after", self.times, "runs calling update", self.N,"times")
        self.assertTrue(within_25_percent > .75)
        
    def test_MorrisCounter_standard_deviation(self):
        random.seed(seed)
        vals = run(MorrisCounter, {}, self.times, self.N)
        within_25_percent = np.mean((self.N - self.N/4 <= vals) & (self.N + self.N/4 >= vals))
        print("\nFor MorrisCounter,", str(within_25_percent * 100)+"% of runs are within 25% on either side of", self.N, "after", self.times, "runs calling update", self.N,"times")
        self.assertTrue(within_25_percent > .75)
        
    def test_MorrisAlpha_standard_deviation(self):
        random.seed(seed)
        vals = run(MorrisAlpha, {}, self.times, self.N)
        within_25_percent = np.mean((self.N - self.N/4 <= vals) & (self.N + self.N/4 >= vals))
        print("\nFor MorrisAlpha,", str(within_25_percent * 100)+"% of runs are within 25% on either side of", self.N, "after", self.times, "runs calling update", self.N,"times")
        self.assertTrue(within_25_percent > .75)
        
    def test_RedisCounter_standard_deviation(self):
        random.seed(seed)
        vals = run(RedisCounter, {}, self.times, self.N)
        within_25_percent = np.mean((self.N - self.N/4 <= vals) & (self.N + self.N/4 >= vals))
        print("\nFor RedisCounter,", str(within_25_percent * 100)+"% of runs are within 25% on either side of", self.N, "after", self.times, "runs calling update", self.N,"times")
        self.assertTrue(within_25_percent > .75)
        

class TestExpectation(unittest.TestCase):
    N = 10000
    times = 100

    def test_Counter_expectation(self):
        average = 0
        for _ in range(self.times):
            c = Counter()
            for _ in range(self.N):
                c.update()
            average += c.query()
        average = average / self.times
        print("\n" + type(c).__name__ + "'s average is", average, "after", self.times, "runs calling update", self.N,"times")
        self.assertTrue(within(average, self.N, self.N * 1/25))
        
    def test_MorrisCounter_expectation(self):
        random.seed(seed)
        average = 0
        for _ in range(self.times):
            c = MorrisCounter()
            for _ in range(self.N):
                c.update()
            average += c.query()
        average = average / self.times
        print("\n" + type(c).__name__ + "'s average is", average, "after", self.times, "runs calling update", self.N,"times")
        self.assertTrue(within(average, self.N, self.N * 1/25))
        
    def test_MorrisAlpha_expectation(self):
        random.seed(seed)
        average = 0
        for _ in range(self.times):
            c = MorrisAlpha()
            for _ in range(self.N):
                c.update()
            average += c.query()
        average = average / self.times
        print("\n" + type(c).__name__ + "'s average is", average, "after", self.times, "runs calling update", self.N,"times")
        self.assertTrue(within(average, self.N, self.N * 1/25))

    def test_RedisCounter_expectation(self):
        random.seed(seed)
        average = 0
        for _ in range(self.times):
            c = RedisCounter()
            for _ in range(self.N):
                c.update()
            average += c.query()
        average = average / self.times
        print("\n" + type(c).__name__ + "'s average is", average, "after", self.times, "runs calling update", self.N,"times")
        self.assertTrue(within(average, self.N, self.N * 1/25))

