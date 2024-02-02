"Solve a maze by recursion with backtracking"
# MCS 275 Spring 2024 Lecture 11
# David Dumas

import maze

def depth_first_maze_solution(M,path=None):
    """
    Take a Maze object `M` and optional partial
    progress `path` (list of Point2 objects) and
    complete to a solution using r.w.b.
    """
    if path == None:
        # if no path given, the path is just 
        # "we're standing at the start"
        path = [M.start]
    if path[-1] == M.goal:
        # this is a solution
        return path
    # enumerate next steps
    possible_next = M.free_neighbors(path[-1])
    if len(path) > 1:
        try:
            possible_next.remove(path[-2])
        except ValueError:
            pass
    # problem: possible_next might contain a
    # point we've visited, so we must remove it
    # if present
    for next_step in possible_next:
        new_path = path + [next_step]
        res = depth_first_maze_solution(M,new_path)
        if res:  # if res is a nonempty list, i.e. not None
            # recursive call found a solution
            return res
    
    # no possible next step worked out.
    return None

if __name__ == "__main__":
    # we're being run as a script
    # generate a random maze
    M = maze.PrimRandomMaze(255,255)
    soln = depth_first_maze_solution(M)
    M.save_png("solved.png",highlight=soln)
    print("Wrote solved.png")