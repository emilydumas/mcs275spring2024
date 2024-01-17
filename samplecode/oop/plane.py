# MCS 275 Spring 2024 Lecture 3 and 4
# David Dumas
"Plane geometry classes"


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
        return "Vector2({},{})".format(self.x, self.y)

    def __repr__(self):
        "Converts an instance to a string, for display to developers"
        return str(self)  # just use the same as __str__

    # A+B becomes A.__add__(B)
    #                  ,----- other summand, e.g. B, need to add to self
    def __add__(self, other):
        "Vector addition"
        if self.verbose:
            print("Vector2.__add__")
        if isinstance(other, Vector2):
            # vec+vec
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            # vec+something else
            return NotImplemented

    def __sub__(self, other):
        "vector subtraction"
        if self.verbose:
            print("Vector2.__sub__")
        # v-w is actually v + (-1)*w
        return self + (-1) * other

    # called to compute self*other
    def __mul__(self, other):
        "Scalar multiplication"
        if self.verbose:
            print("Vector2.__mul__")
        if isinstance(other, float) or isinstance(other, int):
            return Vector2(other * self.x, other * self.y)
        else:
            # refuse to perform this multiplication
            return NotImplemented

    # called to compute other*self after other refuses
    def __rmul__(self, other):
        "reflected scalar multiplication"
        if self.verbose:
            print("__rmul__")
        # tell Python that other*self is the same as self*other
        # i.e 100*v becomes v*100
        return self * other


class Point2:
    "Two-dimensional point specified by coordinates"

    def __init__(self, x, y):
        """
        Initialize a new point with x coordinate `x` and y
        coordinate `y`.
        """
        self.x = x
        self.y = y

    def __str__(self):
        "Converts an instance to a string, for printing"
        return "Point2({},{})".format(self.x, self.y)

    def __repr__(self):
        "Converts an instance to a string, for display to developers"
        return str(self)  # just use the same as __str__

    def __add__(self, other):
        "point + vector is a point"
        if isinstance(other, Vector2):
            return Point2(self.x + other.x, self.y + other.y)
        else:
            return NotImplemented

    # this is responsible for computing other+self
    def __radd__(self, other):
        "vector + point is a point (even though Vector2 is unaware"
        # explicit declaration of commutativity
        return self + other

    # responsible for computing self-other
    def __sub__(self, other):
        "point-point is a vector"
        if isinstance(other, Point2):
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            return NotImplemented
