"Solve a maze by recursion with backtracking"
# MCS 275 Spring 2024 Lecture 11
# Emily Dumas

import maze

# Note: mazes with few walls tend to have loops
# which create problems for the algorithm in
# lecture 11. Since maze.py supports building
# mazes from scratch by adding walls, it seems
# best to have the maze solver allow loops by
# default.  So this module offers both.


def depth_first_maze_solution(M, path=None):
    """
    Take a Maze object `M` and optional partial
    progress `path` (list of Point2 objects) and
    complete to a solution recursively.
    **This function can solve mazes with loops.**
    """
    if path == None:
        # no path given, begin at M.start
        path = [M.start]
    if path[-1] == M.goal:
        # path is a solution, return!
        return path

    # enumerate possible next steps
    possible_next = M.free_neighbors(path[-1])
    # then remove any places we've already been
    possible_next = [x for x in possible_next if x not in path]

    # consider next steps
    for next_step in possible_next:
        new_path = path + [next_step]
        res = depth_first_maze_solution(M, new_path)
        if res:  # if res is a nonempty list, i.e. not None
            # res is in fact a solution; return it
            return res

    # no possible next step worked out
    return None


def depth_first_maze_unique_solution(M, path=None):
    """
    Take a Maze object `M` and optional partial
    progress `path` (list of Point2 objects) and
    complete to a solution recursively.
    **This function CANNOT solve mazes with loops.**
    """
    if path == None:
        # no path given, begin at M.start
        path = [M.start]
    if path[-1] == M.goal:
        # path is a solution, return!
        return path

    # enumerate next steps
    possible_next = M.free_neighbors(path[-1])
    # but don't go backwards
    if len(path) > 1:
        try:
            possible_next.remove(path[-2])
        except ValueError:
            pass
    # consider next steps
    for next_step in possible_next:
        new_path = path + [next_step]
        res = depth_first_maze_unique_solution(M, new_path)
        if res:  # if res is a nonempty list, i.e. not None
            # res is in fact a solution; return it
            return res

    # no possible next step worked out
    return None


if __name__ == "__main__":
    # we're being run as a script
    import sys

    # Allow maze details to be specified as cmd line args
    if len(sys.argv) > 1:
        size = int(sys.argv[1])
    else:
        size = 51
    print("Using size {0}x{0}".format(size))
    if len(sys.argv) > 2:
        fnbase = sys.argv[2]
    else:
        fnbase = "solved_maze"
    print("Using output filenames {0}.png / {0}.svg".format(fnbase))

    # generate a random maze
    M = maze.PrimRandomMaze(size, size)
    # solve
    soln = depth_first_maze_solution(M)
    # save
    print("Writing SVG")
    M.save_svg(fnbase + ".svg", highlight=soln)
    print("Writing PNG")
    M.save_png(fnbase + ".png", highlight=soln)
