"""
@author : Léo Imbert
@created : 14/04/2026
@updated : 14/04/2026
"""

import math

class Vector2:

    def __init__(self, x:int=0, y:int=0):
        self.x, self.y = x, y

    @property
    def mag(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    @property
    def normalized(self):
        m = self.mag
        if m != 0:
            return Vector2(self.x / m, self.y / m)
        return Vector2(0, 0)

    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def __eq__(self, other):
        if not isinstance(other, Vector2):
            raise NotImplemented("Can only compare two Vector2")
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)
    
    def __ne__(self, other):
        if not isinstance(other, Vector2):
            raise NotImplemented("Can only compare two Vector2")
        return not self == other
    
    def __lt__(self, other):
        if not isinstance(other, Vector2):
            raise NotImplemented("Can only compare two Vector2")
        return self.mag < other.mag
    
    def __gt__(self, other):
        if not isinstance(other, Vector2):
            raise NotImplemented("Can only compare two Vector2")
        return self.mag > other.mag
    
    def __le__(self, other):
        if not isinstance(other, Vector2):
            raise NotImplemented("Can only compare two Vector2")
        return self.mag <= other.mag
    
    def __ge__(self, other):
        if not isinstance(other, Vector2):
            raise NotImplemented("Can only compare two Vector2")
        return self.mag >= other.mag
    
    def __neg__(self):
        return Vector2(-self.x, -self.y)
    
    def __add__(self, other):
        if not isinstance(other, Vector2):
            raise NotImplemented("Can only add two Vector2")
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        if not isinstance(other, Vector2):
            raise NotImplemented("Can only substract two Vector2")
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise NotImplemented("Can only multiply Vector2 with int or float")
        return Vector2(self.x * other, self.y * other)
    
    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            raise NotImplemented("Can only divide Vector2 with int or float")
        if other == 0:
            raise ZeroDivisionError("Can't divide by zero")
        return Vector2(self.x / other, self.y / other)
    
    def __iadd__(self, other):
        if not isinstance(other, Vector2):
            raise NotImplemented("Can only add two Vector2")
        self.x += other.x
        self.y += other.y
        return self
    
    def __isub__(self, other):
        if not isinstance(other, Vector2):
            raise NotImplemented("Can only substract two Vector2")
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, other):
        if not isinstance(other, (int, float)):
            raise NotImplemented("Can only multiply Vector2 with int or float")
        self.x *= other
        self.y *= other
        return self

    def __rmul__(self, other):
        return self.__mul__(other)

    def __itruediv__(self, other):
        if not isinstance(other, (int, float)):
            raise NotImplemented("Can only divide Vector2 with int or float")
        if other == 0:
            raise ZeroDivisionError("Can't divide by zero")
        self.x /= other
        self.y /= other
        return self

    def __getitem__(self, key:int):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        
        raise IndexError
    
    def __setitem__(self, key:int, value:int|float):
        if key == 0 and isinstance(value, (int, float)):
            self.x = value
        elif key == 1 and isinstance(value, (int, float)):
            self.y = value
        else:
            raise IndexError
    
    def __iter__(self):
        yield self.x
        yield self.y

    def normalize(self, value:int|float):
        return self.normalized * value
    
    def dot(self, other):
        if not isinstance(other, Vector2):
            raise NotImplemented("Can only calculate the dot product of two Vector2")
        return self.x * other.x + self.y * other.y

if __name__ == "__main__":
    v1 = Vector2(1, 1)
    v2 = Vector2(2, 2)

    v2[1] = 3
    print(v2)