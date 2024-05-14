# MCS 275 Spring 2024 Lecture 17
# Emily Dumas
"Class for storing a set of distinct integers"

from trees import BST


class IntegerSet:
    """
    A collection of distinct integers supporting membership test
    and insert.  (Does not actually perform any type checking,
    so any type supporting comparison will work.)
    """

    def __init__(self, initial_values=None):
        self.T = BST()  # BST as the actual store
        if initial_values:
            for x in initial_values:
                self.insert(x)

    def insert(self, x):
        "Add integer x to the set (do nothing if already there)"
        try:
            self.T.insert(x)
        except ValueError:
            pass

    def __contains__(self, x):
        "Determine whether x is in the set"
        return bool(self.T.search(x))
