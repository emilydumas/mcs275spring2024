# MCS 275 Spring 2024 Lecture 17
# David Dumas
"Classes storing sets of distinct integers"

from trees import BST


class IntegerSetBase:
    "A collection of distinct integers supporting membership test and insert"

    def __init__(self, initial_values=None):
        self._storage_setup()  # should create the needed data structure
        if initial_values:
            for x in initial_values:
                self.insert(x)

    def _storage_setup(self):
        "Internal method to initialize storage structure"
        raise NotImplementedError()

    def insert(self, x):
        "Add integer x to the set (do nothing if already there)"
        if not isinstance(x, int):
            raise TypeError("Only integer elements allowed")
        self._insert_impl(x)  # actual insertion operation

    def _insert_impl(self, x):
        """
        Internal method implementing the actual insert after type check
        meant to be overridden in subclasses
        """
        raise NotImplementedError()

    def __contains__(self, x):
        "Determine whether x is in the set"
        if not isinstance(x, int):
            return False  # non-integers are not there!
        return self._contains_impl(x)

    def _contains_impl(self, x):
        """
        Internal method implementing the actual membership test after type check
        meant to be overridden in subclasses
        """
        raise NotImplementedError()


class IntegerSet(IntegerSetBase):
    """
    A collection of distinct integers supporting membership test and insert
    using a binary search tree as a backing data store
    """

    def _storage_setup(self):
        self.T = BST()  # private storage system is a BST

    def _insert_impl(self, x):
        try:
            self.T.insert(x)
        except ValueError:
            # x was already there.  No problem.
            return

    def _contains_impl(self, x):
        return self.T.search(x) != None


class IntegerSetUL(IntegerSetBase):
    """
    A collection of distinct integers supporting membership test and insert
    using an unordered list as the backing data store
    """

    def _storage_setup(self):
        self.L = []  # unordered list

    def _insert_impl(self, x):
        if x not in self.L:
            self.L.append(x)

    def _contains_impl(self, x):
        return x in self.L


class IntegerSetSL(IntegerSetBase):
    """
    A collection of distinct integers supporting membership test and insert
    using a sorted list as the backing data store
    """

    def _storage_setup(self):
        self.L = []  # will be maintained as a sorted list

    def _insert_impl(self, x):
        # Bisection search to find location where x should go.
        # look at middle value, decide whether x would appear
        # earlier or later
        if not self.L:
            self.L.append(x)
            return
        low = 0
        high = len(self.L) - 1
        while low < high:
            mid = (low + high) // 2
            y = self.L[mid]
            if x == y:
                return
            elif x < y:
                high = mid - 1
            else:
                low = mid + 1
        if x == self.L[low]:
            return
        if x < self.L[low]:
            self.L.insert(low, x)
        else:
            self.L.insert(low + 1, x)

    def _contains_impl(self, x):
        # Bisection search; look at middle value, decide whether
        # the desired element would appear earlier or later
        if not self.L:
            return
        low = 0
        high = len(self.L) - 1
        while low < high:
            mid = (low + high) // 2
            y = self.L[mid]
            if x == y:
                return True
            elif x < y:
                high = mid - 1
            else:
                low = mid + 1
        return x == self.L[low]


if __name__ == "__main__":
    import random
    import time

    n = 20_000
    # n = 200_000
    Linsert = [random.randint(1, 5 * n) for _ in range(n)]
    Lcheck = [random.randint(1, 5 * n) for _ in range(n // 2)] + Linsert[: n // 2]
    random.shuffle(Lcheck)

    implementations = [IntegerSetUL, IntegerSetSL, IntegerSet]

    for cls in implementations:
        print("Testing {} with {} elements:".format(cls.__name__, n))
        t0 = time.time()
        S = cls(Linsert)
        t1 = time.time()
        checks = [x in S for x in Lcheck]
        t2 = time.time()
        print(
            "{:5.2f}s insert          ({:8d} inserts per second)".format(
                t1 - t0, int(n / (t1 - t0))
            )
        )
        print(
            "{:5.2f}s membership test ({:8d} tests per second)".format(
                t2 - t1, int(n / (t2 - t1))
            )
        )


# Annotated sample output of longer-running 200_000 element test
#
# Testing IntegerSetUL with 200000 elements:
# 43.35s insert          (    4613 inserts per second) <-- terrible
# 51.93s membership test (    3851 tests per second)   <-- terrible
# Testing IntegerSetSL with 200000 elements:
#  1.62s insert          (  123221 inserts per second) <-- OK
#  0.26s membership test (  758690 tests per second)   <-- GREAT
# Testing IntegerSet with 200000 elements:
#  0.78s insert          (  256175 inserts per second) <-- GOOD
#  0.64s membership test (  311241 tests per second)   <-- GOOD
