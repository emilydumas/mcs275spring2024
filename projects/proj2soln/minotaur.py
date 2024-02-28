# MCS 275 Spring 2024 Project 2 Solution
# David Dumas
"""
Depth-first search for a solution to Escape of the Minotaur
and related functions checking labyrinths for certain conditions
"""

from plane import Point2
from labyrinth import *


def solution(lab, status, path=None):
    """
    Take a Labyrinth `lab` and status dict `status` and determine
    whether a solution exists under the given conditions.  If so,
    returns one such solution as a list of Point2 objects.  If not,
    returns None.  Uses recursive depth-first search.
    """
    if path == None:
        path = [lab.start]
    possible_next = [x for x in lab.non_wall_neighbors(path[-1]) if x not in path]
    for p in possible_next:
        newstatus = dict(status)  # copy of status
        newpath = path + [p]
        ct = lab.get_cell(p)
        res = None
        # Check for solution
        if ct == CT_GOAL:
            return newpath

        # Check for cell types allowing recursion
        if ct == CT_EMPTY:
            res = solution(lab, newstatus, newpath)
        elif ct == CT_LOCK:
            if newstatus["keys"]:
                newstatus["keys"] -= 1
                res = solution(lab, newstatus, newpath)
        elif ct == CT_PIT:
            if newstatus["plank"]:
                res = solution(lab, newstatus, newpath)
        elif ct == CT_SPRING:
            d = abs(lab.goal - p)
            if d <= newstatus["flight_range"]:
                res = newpath + [lab.goal]

        # res is either a solution or None
        if res:
            return res
        # None means we should try a different next step

    # All next steps failed; return None to indicate backtracking needed
    return None


def has_solution(lab, status):
    "Returns True if Labyrinth `lab` can be solved with status `status`"
    return bool(solution(lab, status))


def optimal_status(lab):
    """
    Given a labyrinth, returns a status dictionary that has a plank
    and enough keys and flight range to make it possible to escape
    *if* any escape is possible.  That is, if
        has_solution(lab,optimal_status(lab))
    returns False, then there are no conditions that allow escape
    from labyrinth `lab`.
    """
    # Include a plank
    d = {"plank": True}
    # Most keys we could possibly need is the number of locks
    d["keys"] = lab.num_locks()
    # Most flight distance we could possibly need is distance between
    # opposite corners of the labyrinth
    corner_NW = Point2(0, 0)
    corner_SE = Point2(lab.xsize, lab.ysize)
    d["flight_range"] = abs(corner_NW - corner_SE)
    return d


def requires_plank(lab):
    """
    Returns True if `lab` can be solved under some conditions but
    is impossible if a plank is absent.
    """
    # Make status giving best chance of escape
    st_optimal = optimal_status(lab)
    # Make a copy of it
    st_no_plank = dict(st_optimal)
    # In the copy, set plank to False
    st_no_plank["plank"] = False
    # "requiring" the plank means you can escape, but if the
    # plank is missing you absolutely cannot.
    return has_solution(lab, st_optimal) and not has_solution(lab, st_no_plank)


def requires_flight(lab: Labyrinth):
    """
    Returns True if `lab` can be solved under some conditions but
    is impossible if flight is not allowed.
    """
    # Make status giving best chance of escape
    st_optimal = optimal_status(lab)
    # Make a copy of it
    st_no_flight = dict(st_optimal)
    # In the copy, set flight range to 0
    st_no_flight["flight_range"] = 0
    # "requiring" the plank means you can escape, but if the
    # flight range is zero you absolutely cannot.
    return has_solution(lab, st_optimal) and not has_solution(lab, st_no_flight)


def min_required_keys(lab):
    """
    Given a labyrinth that can be escaped under some conditions, determines
    the fewest keys that allow escape.
    """
    st = optimal_status(lab)
    if not has_solution(lab, st):
        raise ValueError("Cannot be solved at all!")
    # Keep reducing the number of keys until there is no
    # solution any longer.  Then the previous value was
    # the minimum number required.
    st["keys"] -= 1
    while st["keys"] >= 0 and has_solution(lab, st):
        st["keys"] -= 1
    return st["keys"] + 1
