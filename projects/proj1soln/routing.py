# MCS 275 Spring 2024 Project 1 Solution
# Emily Dumas
"Routing strategies for a factory shipping depot"
import collections.abc
import inspect
from fixtures import CrateQueue

# ---- CLASSES PROVIDED IN STARTER PACK ----
# (i.e. scroll past this for the good stuff)


class Router:
    "Base class for shipping logistics strategies"
    num_input_queues = 5
    required_queue_cls = CrateQueue

    def __init__(self, input_queues):
        "Prepare a new empty queue"
        # Input_queues validation
        # Is it a list (or tuple)?
        if isinstance(input_queues, str) or not isinstance(
            input_queues, collections.abc.Sequence
        ):
            raise TypeError(
                "argument `input_queues` must be list or tuple of objects of type `{}`".format(
                    self.required_queue_cls.__name__
                )
            )
        # Are any of the elements class names
        # (a common mistake) or of the wrong
        # type?
        for x in input_queues:
            if inspect.isclass(x):
                raise TypeError(
                    "each item in `input_queues` must be an instance; instead, a class was found: {}".format(
                        x.__class__.__name__,
                    )
                )
            if not isinstance(x, self.required_queue_cls):
                raise TypeError(
                    "each item in `input_queues` must be a `{}` object; this item is not: {}".format(
                        self.required_queue_cls.__name__,
                        repr(x),
                    )
                )
        # Does input_queues have the right length
        if len(input_queues) != self.num_input_queues:
            raise ValueError(
                "argument `input_queues` has length {} instead of required length {}".format(
                    len(input_queues), self.num_input_queues
                )
            )
        # Validation succeeded; store as attribute
        self.input_queues = input_queues

    def prepare_load(self):
        "Examine the queues and select items for the next truck"
        raise NotImplementedError()

    def __str__(self):
        "Human-readable string representation"
        return self.__class__.__name__ + "()"

    def __repr__(self):
        "Developer-readable string representation"
        return str(self)


class OldRouter(Router):
    "Router that only uses the first three queues"

    def prepare_load(self):
        "Take <=1 crate from queues 0,1,2"
        L = []
        for q in self.input_queues[:3]:
            if q:
                L.append(q.pop())
        return L


# ---- END OF CLASSES PROVIDED IN THE STARTER PACK ----


class BreadthRouter(Router):
    """
    Router that tries to take one crate from each queue in order,
    stopping as soon as it has gathered three.
    """

    def prepare_load(self):
        L = []  # for return value
        # Check the queues in order
        for Q in self.input_queues:
            if Q:  # "if Q" means "if Q is not empty" (see CrateQueue.__bool__)
                L.append(Q.pop())  # Take one crate and add to return list
            if len(L) == 3:
                # We have three, so we're done
                break
        return L


class CyclingDepthRouter(Router):
    """
    Router that lets the queues take turns being the "active one" in a cycle
    (0,1,2,3,4,0,1,...).  Always tries to take 3 crates from the active one.
    """

    def __init__(self, input_queues):
        super().__init__(input_queues)
        self.reset()  # initializes self.active_queue which stores index

    def prepare_load(self):
        Q = self.input_queues[self.active_queue]  # active queue object
        L = []  # for return value
        while Q and len(L) < 3:  # Stop if Q empty OR if L grows to size 3
            L.append(Q.pop())  # Take one from Q
        # Advance active_queue to the next one (for subsequent prepare_load call)
        self.active_queue = (self.active_queue + 1) % len(self.input_queues)
        return L

    def reset(self):
        "Set the active queue index back to index 0"
        self.active_queue = 0

    # Having __str__ is helpful for debugging but was not required
    def __str__(self):
        return "{}(active_queue={})".format(self.__class__.__name__, self.active_queue)


class FillPriorityRouter(Router):
    """
    Routing strategy that takes three crates according to a fixed strategy:
    The next crate is always taken from the queue with the least empty space.
    Ties are resolved by using the queue with smaller index.
    """

    def prepare_one(self):
        "Remove and return one crate from the queue with the least empty space"
        nonempties = [q for q in self.input_queues if q]  # nonempty queue objects
        # Now we want to find one with the least empty space.  We could use a for
        # loop and keep track of the least space seen so far, but there is also
        # the built-in min() function which can do this.  It resolves ties in the
        # way specified: Preferring the one appearing earlier in the list.  The
        # key=... argument specifies the function that gets applied to list elements
        # before comparing them.
        #
        # Thus the next line means "let Q be the one with least empty space"
        Q = min(nonempties, key=lambda x: x.remaining_space())
        # NOTE: If `nonempties` is an empty list (i.e. all queues are empty)
        # then min() will raise an exception.  We catch this in `prepare_load`
        # below
        return Q.pop()  # take and return one from Q

    def prepare_load(self):
        L = []
        try:
            # Three times, we try to get a crate using the strategy
            for _ in range(3):
                L.append(self.prepare_one())
        except (IndexError, ValueError):
            # If we land here, it means all the queues were empty
            # so min() in prepare_one raised an exception.  That
            # interrupts the for-loop just as we'd like, so we
            # just ignore the exception.
            pass
        return L


class BalanceRouter(Router):
    """
    Routing strategy that takes three crates according to a fixed strategy:
    The next crate is always taken from the queue that the router has taken
    the fewest crates from up to that point.  Ties are resolved by preferring
    the queue with smaller index.
    """

    def __init__(self, input_queues):
        super().__init__(input_queues)
        self.reset()  # initializes history

    def prepare_one(self):
        """
        Remove and return one crate from the queue that we've taken the
        fewest crates from thus far.
        """
        # Make a list of the indices (0..4) that correspond to queues
        # that are not empty.
        nonempty_indices = [i for i, q in enumerate(self.input_queues) if q]
        # Of these indices, which one corresponds to the queue we've taken
        # the fewest from?  (As before this use of min() and key=... could be
        # replaced by a for loop that checks the whole list nonempty_indices
        # while keeping track of the smallest shipcount seen.)
        idx = min(nonempty_indices, key=lambda i: self.shipcount[i])
        # Now we know the index of the queue we want.
        Q = self.input_queues[idx]  # Get the queue object to take from
        c = Q.pop()  # Take a crate
        self.shipcount[idx] += 1  # Record that a crate was taken
        return c  # return the crate we took

    def prepare_load(self):
        L = []
        try:
            # Take a single crate three times
            # adding to L as we go
            for _ in range(3):
                L.append(self.prepare_one())
        except (IndexError, ValueError):
            # Just as in FillPriorityRouter, catching this
            # exception and doing nothing has the effect of
            # making the for loop exit early if the queues
            # are all empty (which is the intended behavior)
            pass
        return L

    def reset(self):
        "Initialize the history of crates taken from each queue"
        # self.shipcount[i] is the number of crates taken from self.input_queues[i]
        # so initially it is just a list of zeros
        self.shipcount = [0 for _ in self.input_queues]

    # Having __str__ is helpful for debugging but was not required
    def __str__(self):
        return "{}(taken_counts={})".format(
            self.__class__.__name__, repr(self.shipcount)
        )
