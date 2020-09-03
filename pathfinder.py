"""Controls:
    - First place start and end nodes
        - Click to place start
        - Click again to place end
    - Drag and click to draw walls
    - Press m key to generate maze
    - Press s key to deploy A* algorithm
    - Press d key to deploy Dijkstra's algorithm
    - Press c to reset the game
    - Right click to erase
"""

import pygame
import random
import math as m
from queue import PriorityQueue

pygame.init()

height = 45*17
width = 45*17
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pathfinder")

# define some colours for later
dark_gray = [75, 75, 76]
lite_gray = [200, 200, 200]
white = [255, 255, 255]
black = [0, 0, 0]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
yellow = [255, 255, 0]
purple = [128, 0, 128]
orange = [255, 165, 0]
cyan = [64, 224, 208]



class Node:
    # define methods to get/change state of node
    def __init__(self, row, col, height, total_rows):
        self.row = row
        self.col = col
        self.x = row * height
        self.y = col * height
        self.colour = lite_gray
        self.neighbours = []
        self.width = height
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        # we will say that if node is cyan then it is closed
        return self.colour == cyan

    def is_open(self):
        # we will say that if node is blue then it is open
        return self.colour == blue

    def is_wall(self):
        # we will say that if node is black then it is a wall
        return self.colour == black

    def is_end(self):
        # we will say that if node is red then it is the end
        return self.colour == red

    def is_start(self):
        # we will say that if node is green then it is the start
        return self.colour == green

    def reset(self):
        # to reset grid
        self.colour = lite_gray

    def make_closed(self):
        # make closed by making node cyan
        self.colour = cyan

    def make_open(self):
        # make open by making node blue
        self.colour = blue

    def make_wall(self):
        # make wall by making node black
        self.colour = black

    def make_end(self):
        # make end by making node red
        self.colour = red

    def make_start(self):
        # make start by making node green
        self.colour = green

    def make_path(self):
        # make path by making node white
        self.colour = white

    def draw(self, window):
        pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbour(self, grid):
        # find all neighbours of node and add them to list
        self.neighbours = []
        # check we arent on edge of grid and adjacent square down isn't barrier

        # Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbours.append(grid[self.row - 1][self.col])

        # Down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbours.append(grid[self.row + 1][self.col])

        # Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbours.append(grid[self.row][self.col - 1])

        # Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbours.append(grid[self.row][self.col + 1])

    def __lt__(self, other):
        return False

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

# define heuristic function as euclidean distance
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return m.sqrt((abs(x1 - x2) ** 2) + (abs(y1 - y2) ** 2))

def draw_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def astar(draw, grid, start, end):
    count = 0
    # priority queue uses heap sort algorithm to get the smallest element out of the queue efficiently
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    # track where we were
    came_from = {}
    # current shortest distance from start to each node
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    # shortest distance from start to node + estimate to end
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    # need to use dictionary to check if node in the queue
    open_set_hash = {start}

    while not open_set.empty():
        # while we have nodes in the queue
        for event in pygame.event.get():
            # in case we need to escape
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]  # index at 2 to get node
        open_set_hash.remove(current)

        if current == end:
            draw_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True  # if we have found the end, make path

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:  # if new path is better, replace it
                came_from[neighbour] = current
                # calc new f and g score
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    # check if neighbour is in the queue
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        draw()

        if current != start:
            # if the node we just considered is not start, make closed
            current.make_closed()
    return False

def dijkstra(draw, grid, start, end):
    count = 0
    # priority queue uses heap sort algorithm to get the smallest element out of the queue efficiently
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    # track where we were
    came_from = {}
    # current shortest distance from start to each node
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    # need to use dictionary to check if node in the queue
    open_set_hash = {start}

    while not open_set.empty():
        # while we have nodes in the queue
        for event in pygame.event.get():
            # in case we need to escape
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]  # index at 2 to get node
        open_set_hash.remove(current)

        if current == end:
            draw_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True  # if we have found the end, make path

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:  # if new path is better, replace it
                came_from[neighbour] = current
                # calc new f and g score
                g_score[neighbour] = temp_g_score
                if neighbour not in open_set_hash:
                    # check if neighbour is in the queue
                    count += 1
                    open_set.put((g_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        draw()

        if current != start:
            # if the node we just considered is not start, make closed
            current.make_closed()
    return False

def make_grid(rows, wid):
    grid = []
    gap = wid // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def draw(window, grid):
    # Updated/drawn on every pass
    window.fill(dark_gray)

    for row in grid:
        for node in row:
            node.draw(window)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


# main function
def main(win, height):
    rows = 45
    grid = make_grid(rows, height)

    start = None
    end = None

    running = True
    while running:
        draw(win, grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:  # left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, height)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_wall()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, height)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbour(grid)
                    astar(lambda: draw(win, grid), grid, start, end)

                if event.key == pygame.K_d and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbour(grid)
                    dijkstra(lambda: draw(win, grid), grid, start, end)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        draw_maze(rows, grid)
                        for row in grid:
                            for node in row:
                                node.update_neighbour(grid)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(rows, height)

    pygame.quit()

main(window, height)