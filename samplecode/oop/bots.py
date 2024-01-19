"""Classes representing robots in a simulation"""
# MCS 275 Spring 2024 David Dumas
# Lecture 5

import plane
import random


class Bot:
    """Base class for all robots.  Sits in one place forever."""

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

    def update(self):
        "Take one step, randomly"
        possible_steps = [
            plane.Vector2(1, 0),
            plane.Vector2(-1, 0),
            plane.Vector2(0, 1),
            plane.Vector2(0, -1),
        ]
        step = random.choice(possible_steps)
        self.move_by(step)


class DestructBot(Bot):
    """Robot that sits in one place for a while and then deactivates"""

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
        "Deactivate if it's time"
        if self.active:
            self.remaining_time -= 1
            if self.remaining_time == 0:
                self.active = False
