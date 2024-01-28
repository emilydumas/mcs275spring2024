# MCS 275 Spring 2024 Project 1 Starter Pack
"Classes representing factory products and storage queues"

import collections


class Crate:
    """
    A finished crate containing a manufactured part.
    WARNING: In `Router` subclasses: Do not access any
    attributes, call any methods, or instantiate this class.
    """

    def __init__(self, label):
        "Initialize crate with a given label"
        self.label = label  # secret attribute, don't access in routing.py

    def __str__(self):
        "Human-readable string representation"
        return "{}(label={})".format(self.__class__.__name__, repr(self.label))

    def __repr__(self):
        "Developer-readable string representation"
        return str(self)


class CrateQueue:
    """
    Queue representing storage area for Crates that
    come off a production line
    """
    msg_cls = Crate

    def __init__(self, contents=None, maxlen=3):

        self.items = collections.deque(maxlen=maxlen)
        self.maxlen = maxlen
        if contents is not None:
            for c in contents:
                self.insert(c)

    def is_nonempty(self):
        "Is there at least one Crate in this queue?"
        return bool(self.items)

    def is_empty(self):
        "Is this queue empty?"
        return not self.is_nonempty()

    def __bool__(self):
        "Is there at least one Crate in this queue?"
        return self.is_nonempty()

    def __len__(self):
        "Return number of Crate objects in queue"
        return len(self.items)

    def is_full(self):
        "Is the queue full?"
        return len(self) == self.maxlen

    def remaining_space(self):
        """
        How many Crate objects can be added before
        this queue is full?
        """
        return self.maxlen - len(self)

    def pop(self):
        "Remove and return the next waiting Crate"
        try:
            return self.items.pop()
        except IndexError as e:
            raise IndexError("pop called on empty {}".format(self.__class__.__name__)) from e

    def peek(self):
        "Return (but do not remove) next waiting Crate"
        try:
            return self.items[-1]
        except IndexError as e:
            raise IndexError("peek called on empty {}".format(self.__class__.__name__)) from e

    def insert(self, item, raise_on_full=False):
        "Add an item to the queue; FORBIDDEN TO BE USED IN ROUTING"
        if not isinstance(item, self.msg_cls):
            raise ValueError(
                "Can only insert items of class {}".format(self.msg_cls.__name__)
            )
        try:
            self.items.insert(0, item)
        except IndexError as e:
            if raise_on_full:
                raise IndexError(
                    "Attempt to insert into full {}".format(self.__class__.__name__)
                ) from e

    def __str__(self):
        "Human-readable string representation"
        return "{}({})".format(self.__class__.__name__, repr(list(self.items)))

    def __repr__(self):
        "Developer-readable string representation"
        return str(self)
