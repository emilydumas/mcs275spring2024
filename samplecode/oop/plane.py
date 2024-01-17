# MCS 275 Spring 2024 Lectures 3 and 4
# David Dumas
"Plane geometry classes"

import math


class Vector2:
    "Two-dimensional vector specified by components"

    def __init__(self, x, y, verbose=False):
        """
        Initialize a new vector with x component `x` and y
        component `y`.
        """
        self.x = x
        self.y = y
        self.verbose = verbose

    def __str__(self):
        "Converts an instance to a string, for printing"
        return "{}({},{})".format(self.__class__.__name__, self.x, self.y)

    def __repr__(self):
        "Converts an instance to a string, for display to developers"
        return str(self)  # just use the same as __str__

    # A+B becomes A.__add__(B)
    #                  ,----- other summand, e.g. B, need to add to self
    def __add__(self, other):
        "Vector addition"
        if self.verbose:
            print("Vector2.__add__ called with self={} other={}".format(self, other))
        if isinstance(other, Vector2):
            # vec+vec
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, Point2):
            # vec+point
            return Point2(self.x + other.x, self.y + other.y)
        else:
            # anything else
            return NotImplemented

    # Handles a request to multiply self*other (should return answer)
    # expect other to be a number (float, int)
    def __mul__(self, other):
        "Scalar multiplication self*other"
        print("__mul__ called")
        if isinstance(other, int) or isinstance(other, float):
            # other is a float or int, so we can do scalar mult
            return Vector2(other * self.x, other * self.y)
        else:
            # other is not a float or int, so refuse
            return NotImplemented

    def __rmul__(self, other):
        "Scalar multiplication (called when operation other*self fails)"
        if self.verbose:
            print("__rmul__ called")
        return self * other  # will call __mul__

    def __sub__(self, other):
        "Vector subtraction"
        if self.verbose:
            print("__sub__ called")
        # declare that self-other is actually self + (-1)*other
        return self + (-1) * other

    def __abs__(self):
        "absolute value is the length"
        return math.sqrt(self.x**2 + self.y**2)


class Point2:
    "Point in the plane specified by coordinates"

    def __init__(self, x, y, verbose=False):
        """
        Initialize a new point with x coord `x` and y
        coord `y`.
        """
        self.x = x
        self.y = y
        self.verbose = verbose

    def __str__(self):
        "Converts an instance to a string, for printing"
        return "{}({},{})".format(self.__class__.__name__, self.x, self.y)

    def __repr__(self):
        "Converts an instance to a string, for display to developers"
        return str(self)  # just use the same as __str__

    def __sub__(self, other):
        "point - point is a vector, subtract corresponding coords"
        if isinstance(other, Point2):
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            return NotImplemented

    # A+B will call A.__add__(B)
    def __add__(self, other):
        "point+vector addition"
        if self.verbose:
            print("__add__ called")
        if isinstance(other, Vector2):
            return Point2(self.x + other.x, self.y + other.y)
        else:
            return NotImplemented
