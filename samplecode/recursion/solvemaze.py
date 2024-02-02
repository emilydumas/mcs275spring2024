"Recursion with backtracking to solve a maze"
# MCS 275 Spring 2024
# David Dumas

def depth_first_maze_solution(M,path=None):
    "Solve Maze `M` using recursion"
    if path == None:
        # first call, start at M.start
        path = [M.start]
    if path[-1] == M.goal:
        # path is a solution, return it
        return path
    possible_next = M.free_neighbors(path[-1])
    # no loops, so the only step we're not allowed
    # is path[-2], which might not exist
    if len(path) > 1:
        try:
            possible_next.remove(path[-2])
        except ValueError:
            pass
    for next_step in possible_next:
        new_path = path + [next_step]
        res = depth_first_maze_solution(M,new_path)
        if res:
            return res
    return None # backtrack!

if __name__=="__main__":
    # demo
    import maze
    M = maze.PrimRandomMaze(255,255)
    soln = depth_first_maze_solution(M)
    M.save_png("solved.png",highlight=soln)
    print("Saved solved.png")