from typing import List, Any


def M(X: 'Vector'):
    return sum(X) / len(X)

def D(X: 'Vector'):
    return M(X**2) - M(X)**2

def r(X: 'Vector', Y: 'Vector'):
    return (X - X.average)*(Y - Y.average) / (sum((X - X.average)**2) * sum((Y - Y.average)**2))**(1/2)



class Vector:
    def __init__(self, value=None):
        self.value = value or []
        if len(self.value) > 0:
            self.average = sum(self.value) / len(self.value)
        else:
            self.average = 0

    def __getitem__(self, key):
        return self.value[key]

    def __iter__(self):
        return self.value.__iter__()

    def __len__(self):
        return len(self.value)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__([self[i] + other[i] for i in range(len(self))])
        elif isinstance(other, int) or isinstance(other, float):
            return self.__class__([i + other for i in self])

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__([self[i] - other[i] for i in range(len(self))])
        elif isinstance(other, int) or isinstance(other, float):
            return self.__class__([i - other for i in self])

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return sum([self[i] * other[i] for i in range(len(self))])
        elif isinstance(other, int) or isinstance(other, float):
            return self.__class__([i * other for i in self])

    def __pow__(self, power):
        return self.__class__([i**power for i in self])

    def append(self, other):
        self.average = (self.average * self.len() + other) / (self.len() + 1)
        self.value.append(other)

    def sum(self):
        return sum(self.value)

    def len(self):
        return len(self.value)

    def __str__(self):
        return str(self.value)
