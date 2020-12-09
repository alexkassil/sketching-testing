import random
import math

class Counter:
    def __init__(self):
        self.X = 0
    def update(self):
        self.X += 1
    def query(self):
        return self.X

    
class MorrisCounter:
    def __init__(self, bits=8):
        self.X = 0
        self.bits = bits
    def update(self):
        if self.X < (2 ** self.bits) - 1 and \
           random.random() < 1/(2 ** self.X):
            self.X += 1
    def query(self):
        return (2 ** self.X) - 1


class MorrisAlpha:
    def __init__(self, a=.05, bits=8, default=5):
        self.X = 0
        self.a = a
        self.bits = bits
        self.default = default
    def update(self):
        if self.X < self.default:
            self.X += 1
        elif self.X < (2 ** self.bits) - 1 and \
             random.random() < 1/((1 + self.a)**self.X):
            self.X += 1
    def query(self):
        if self.X <= self.default:
            return self.X
        return 1/self.a * (((1 + self.a)**self.X) - 1)

class ApproxCountOld:
    C = .001
    def __init__(self, eps=.01, delta=.05):
        self.TX = 0
        self.delta = delta
        self.eps = eps
        self.n = delta
        self.X_0 = math.ceil(math.log( self.C * math.log(1 / self.n) / (self.eps ** 3), 1+self.eps))
        self.Y = 0
        self.X = self.X_0
        self.a = 1
        self.T = math.ceil((1 + self.eps) ** self.X)

    def update(self):
        self.TX += 1
        if random.random() < self.a:
            self.Y += 1
        
        if self.Y > self.a * self.T:
            self.X += 1
            self.T = math.ceil((1 + self.eps) ** self.X)
            a_new = (self.C * math.log(1 / self.n)) / ((self.eps ** 3) * self.T)
            self.Y = math.floor((self.Y * a_new) / self.a)
            self.a = a_new

    def query(self):
        #print(self.TX, self.Y, self.X, self.X_0, self.T)
        if self.X == self.X_0:
            return self.Y
        else:
            return self.T

class ApproxCount:
    C = .001
    def __init__(self, eps=.01, delta=.05):
        self.TX = 0
        self.delta = delta
        self.eps = eps
        self.n = delta
        self.X_0 = math.ceil(math.log( self.C * math.log(1 / self.n) / (self.eps ** 3), 1+self.eps))
        self.Y = 0
        self.X = self.X_0
        self.a = 1
        self.T = math.ceil((1 + self.eps) ** self.X)

    def update(self):
        self.TX += 1
        
        if self.Y > self.a * self.T:
            self.X += 1
            self.T = math.ceil((1 + self.eps) ** self.X)
            self.n = (self.C * self.delta) / (self.eps ** 2)
            #a_new = (self.C * math.log(1 / self.n)) / ((self.eps ** 3) * self.T)
            a_new = min(1, (self.C * math.log(1/self.n)) / ((self.eps ** 3) * self.T))
            self.Y = math.floor((self.Y * a_new) / self.a)
            self.a = a_new
        else:
            if random.random() < self.a:
                self.Y += 1

    def query(self):
        #print(self.TX, self.Y, self.X, self.X_0, self.T)
        if self.X == self.X_0:
            return self.Y
        else:
           return self.T

class RedisCounter:
    def __init__(self, a=10, default=5, bits=8):
        self.a = a
        self.default = default
        self.X = 0
        self.bits = bits

    def update(self):
        if self.X != (2 ** self.bits) - 1:
            r = random.random()
            baseval = self.X - self.default
            if baseval < 0:
                baseval = 0
            p = 1/(baseval * self.a + 1)
            if r < p:
                self.X += 1

    def query(self):
        if self.X <= self.default:
            return self.X
        return self.a / 2 * (self.X - self.default) ** 2
