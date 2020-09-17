def draw_maze(rows, grid):
    # make all nodes a wall
    for row in grid:
        for node in row:
            node.make_wall()
    # choose start point and make it not wall
    # define start point
    current = grid[1][1]
    # make start node not a wall
    current.reset()
    # create a stack and put the start node in it
    # we will use this to backtrack
    stack = []
    draw_branch(current, rows, grid, stack)

def draw_branch(current, rows, grid, stack):
    # determine squares which are valid paths
    paths = []
    # check we arent on edge of grid and 2-away square down is still wall

    # Up
    if current.row > 1 and grid[current.row - 2][current.col].is_wall():
        paths.append([grid[current.row - 2][current.col], grid[current.row - 1][current.col]])

    # Down
    if current.row < current.total_rows - 2 and grid[current.row + 2][current.col].is_wall():
        paths.append([grid[current.row + 2][current.col], grid[current.row + 1][current.col]])

    # Left
    if current.col > 1 and grid[current.row][current.col - 2].is_wall():
        paths.append([grid[current.row][current.col - 2], grid[current.row][current.col - 1]])

    # Right
    if current.col < current.total_rows - 2 and grid[current.row][current.col + 2].is_wall():
        paths.append([grid[current.row][current.col + 2], grid[current.row][current.col + 1]])

    # if we have a path to choose from
    if paths != []:
        # choose a path at random
        path = random.choice(paths)
        # make it not a wall
        for node in path:
            node.reset()
        draw(window, grid)
        # move current node
        current = path[0]
        stack.append(current)
        draw_branch(current, rows, grid, stack)
    elif len(stack) > 0:
        current = stack[0]
        stack.pop(0)
        draw_branch(current, rows, grid, stack)
    else:
        return True
