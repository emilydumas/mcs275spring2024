# MCS 275 Spring 2024 Lectures 3 and 4
# David Dumas
"Plane geometry classes"

# NOTE: All the .verbose and print() stuff in the methods below is used to
# show which special methods get called.  It's here because this lecture
# example was intended to illustrate how overloading works.

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
        if self.verbose:
            print("called: {}.__str__".format(self.__class__.__name__))
        return "{}({},{})".format(self.__class__.__name__, self.x, self.y)

    def __repr__(self):
        "Converts an instance to a string, for display to developers"
        if self.verbose:
            print("called: {}.__repr__".format(self.__class__.__name__))
        return str(self)  # just use the same as __str__

    # A+B becomes A.__add__(B)
    #                  ,----- other summand, e.g. B, need to add to self
    def __add__(self, other):
        "Vector addition"
        if self.verbose:
            print("called: {}.__add__".format(self.__class__.__name__))
        if isinstance(other, Vector2):
            # vec+vec
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            # anything else
            return NotImplemented

    # Handles a request to multiply self*other (should return answer)
    # expect other to be a number (float, int)
    def __mul__(self, other):
        "Scalar multiplication self*other"
        if self.verbose:
            print("called: {}.__mul__".format(self.__class__.__name__))
        if isinstance(other, int) or isinstance(other, float):
            # other is a float or int, so we can do scalar mult
            return Vector2(other * self.x, other * self.y)
        else:
            # other is not a float or int, so refuse
            return NotImplemented

    def __rmul__(self, other):
        "Scalar multiplication (called when operation other*self fails)"
        if self.verbose:
            print("called: {}.__rmul__".format(self.__class__.__name__))
        return self * other  # will call __mul__

    def __sub__(self, other):
        "Vector subtraction"
        if self.verbose:
            print("called: {}.__sub__".format(self.__class__.__name__))
        # declare that self-other is actually self + (-1)*other
        return self + (-1) * other

    def __abs__(self):
        "absolute value is the length"
        if self.verbose:
            print("called: {}.__abs__".format(self.__class__.__name__))
        return math.sqrt(self.x**2 + self.y**2)

    def __eq__(self, other):
        "equality means both coordinates are the same"
        # TODO: Consider whether to type-check `other`
        return self.x == other.x and self.y == other.y


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
        if self.verbose:
            print("called: {}.__str__".format(self.__class__.__name__))
        return "{}({},{})".format(self.__class__.__name__, self.x, self.y)

    def __repr__(self):
        "Converts an instance to a string, for display to developers"
        if self.verbose:
            print("called: {}.__repr__".format(self.__class__.__name__))
        return str(self)  # just use the same as __str__

    def __sub__(self, other):
        "point - point is a vector, subtract corresponding coords"
        if isinstance(other, Point2):
            return Vector2(self.x - other.x, self.y - other.y)
        elif isinstance(other, Vector2):
            # point-vector should be reduced to point + (-1)*vector
            return self + (-1) * other
        else:
            return NotImplemented

    # A+B will call A.__add__(B)
    def __add__(self, other):
        "point+vector addition"
        if self.verbose:
            print("called: {}.__add__".format(self.__class__.__name__))
        if isinstance(other, Vector2):
            return Point2(self.x + other.x, self.y + other.y)
        else:
            return NotImplemented

    # vec+point will call Vector2.__add__, fail, then call Point2.__radd__ below
    # with "other" being the Vector2
    def __radd__(self, other):
        "vector+point addition"
        if self.verbose:
            print("called: {}.__radd__".format(self.__class__.__name__))
        # declare that it's just the same as point+vec
        return self + other  # will call Point2.__add__

    def __eq__(self, other):
        "equality means both coordinates are the same"
        # TODO: Consider whether to type-check `other`
        return self.x == other.x and self.y == other.y
