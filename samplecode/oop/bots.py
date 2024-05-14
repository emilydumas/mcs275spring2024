"""Classes representing robots in a simulation"""
# MCS 275 Spring 2024 Emily Dumas
# Lectures 5-6

import plane
import random


class Bot:
    """Base class for all robots.  Sits in one place forever."""

    symbol = "B"  # character used to represent in botsimulation_fancy

    def __init__(self, position):
        """Setup with initial position `position` (a plane.Point2 instance)"""
        self.active = True
        if not isinstance(position, plane.Point2):
            raise TypeError("Bot position must be a Point2")
        self.position = position

    def move_by(self, v):
        "Move the position of this Bot by Vector2 `v`"
        self.position = self.position + v

    def __str__(self):
        """Human-readable string representation"""
        return "{}(position={},active={})".format(
            self.__class__.__name__,
            self.position,
            self.active,
        )

    def __repr__(self):
        """Unambiguous string representation"""
        return str(self)

    def update(self):
        """Advance one time step (do nothing in this case)"""


class WanderBot(Bot):
    """Robot that moves randomly (up,down,left,right)"""

    symbol = "W"
    possible_steps = [  # class attribute
        plane.Vector2(1, 0),
        plane.Vector2(-1, 0),
        plane.Vector2(0, 1),
        plane.Vector2(0, -1),
    ]

    def update(self):
        "Take one step, randomly"
        step = random.choice(self.possible_steps)
        self.move_by(step)


class FastWanderBot(WanderBot):
    "Similar to WanderBot but can move diagonally"
    symbol = "F"
    possible_steps = [
        plane.Vector2(1, 0),
        plane.Vector2(-1, 0),
        plane.Vector2(0, 1),
        plane.Vector2(0, -1),
        plane.Vector2(1, 1),
        plane.Vector2(1, -1),
        plane.Vector2(-1, 1),
        plane.Vector2(-1, -1),
    ]


class DestructBot(Bot):
    """Robot that sits in one place for a while and then deactivates"""

    symbol = "D"

    def __init__(self, position, active_time):
        """
        Initialize a DestructBot that remains active
        for `active_time` steps
        """
        # Call the Bot constructor
        super().__init__(position)

        # Do DestructBot-specific initialization
        self.active_time = active_time  # never changes
        self.remaining_time = active_time  # decreases by 1 each update

    def update(self):
        "Deactivate if active_time has elapsed"
        if self.active:
            self.remaining_time -= 1
            if self.remaining_time == 0:
                self.active = False


class PatrolBot(Bot):
    """Robot walks back and forth along a straight line segment"""

    symbol = "P"
    state_transitions = {
        "out": "back",
        "back": "out",
    }

    def __init__(self, position, direction, steps):
        """
        Initialize a robot at `position` that takes `steps`
        steps in `direction` then turns around, repeats.
        """
        # Call Bot constructor
        super().__init__(position)
        # Do Patrol-specific initialization
        self.vectors = {
            "out": direction,
            "back": (-1) * direction,
        }
        self.steps = steps  # constant
        self.state = "out"  # either "out" or "back"
        self.n = 0  # number of steps so far in the current state

    def update(self):
        "Take a step and turn around if appropriate"
        # Take a step
        self.move_by(self.vectors[self.state])
        self.n += 1
        # Is it time to turn around?
        if self.n == self.steps:
            # indeed, turn around
            self.n = 0
            self.state = self.state_transitions[self.state]
