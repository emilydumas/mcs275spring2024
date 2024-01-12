# MCS 275 Spring 2024 Lecture 3
# David Dumas
"Plane geometry classes"

class Vector2:
    "Two-dimensional vector specified by components"
    def __init__(self,x,y):
        """
        Initialize a new vector with x component `x` and y
        component `y`.
        """
        self.x = x
        self.y = y

    def __str__(self):
        "Converts an instance to a string, for printing"
        return "Vector2({},{})".format(self.x,self.y)

    def __repr__(self):
        "Converts an instance to a string, for display to developers"
        return str(self) # just use the same as __str__
    
    # A+B becomes A.__add__(B)
    #                  ,----- other summand, e.g. B, need to add to self
    def __add__(self,other):
        "Vector addition"
        print("Vector2.__add__ called with self={} other={}".format(self,other))
        return Vector2(self.x+other.x, self.y+other.y)
