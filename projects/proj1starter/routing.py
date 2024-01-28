# MCS 275 Spring 2024 Project 1 Starter Pack
# 1. ADD CLASSES TO THE END OF THIS FILE
# 2. REPLACE THESE COMMENTS WITH HEADER
# 3. SUBMIT THIS FILE AND NOTHING ELSE

# --- start of area you shouldn't edit ---
"Routing strategies for a factory shipping depot"
import collections.abc
import inspect
from fixtures import Crate, CrateQueue


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
                        self.required_queue_cls.__name__,
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

# --- end of area you shouldn't edit ---

# Add subclasses here!
