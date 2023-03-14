"""
author: Sam Tebbet
description: Coursework for ECM2423 Artificial Intelligence
"""

import time
from PIL import Image, ImageDraw
import sys
from collections import deque

sys.setrecursionlimit(100000)


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0.0
        self.h = 0.0
        self.f = 0.0
        self.parent = None
        self.visited = False

    def get_position(self):
        return self.x, self.y


def get_manhattan(current_node: Node, end_node: Node):
    return abs(current_node.x - end_node.x) + abs(current_node.y - end_node.y)


def generate_successors(maze, q: Node) -> [Node]:
    neighbours = get_neighbours(q.get_position(), maze)
    successors = []
    for neighbour in neighbours:
        successor = Node(neighbour[0], neighbour[1])
        successor.parent = q
        successors.append(successor)
    return successors


def a_star_algorithm(maze, start, end):
    open_list = deque()
    closed_list = deque()

    q = Node(0, 0)
    open_list.append(start)
    while open_list:
        # Find the node with the least f
        current_min = 10000000
        for node in open_list:
            if node.f < current_min:
                q = node

        # Remove q from the open list
        open_list.remove(q)
        # Generate q's successors
        successors = generate_successors(maze, q)

        for successor in successors:
            # If the successor is the goal, stop search
            if successor.get_position() == end.get_position():
                return closed_list, True
            successor.g = q.g + get_manhattan(successor, q)
            successor.h = get_manhattan(successor, end)
            successor.f = successor.g + successor.h

            to_skip = False
            for open_node in open_list:
                if open_node.get_position() == successor.get_position() and open_node.f < successor.f:
                    to_skip = True
            for closed_node in closed_list:
                if closed_node.get_position() == successor.get_position() and closed_node.f < successor.f:
                    to_skip = True

            if not to_skip:
                open_list.append(successor)
        closed_list.append(q)
    return closed_list, False


def get_neighbours(node: (int, int), maze: [[str]]):
    x_coord = node[0]
    y_coord = node[1]
    width = len(maze[0])
    height = len(maze)
    paths = []
    if (y_coord - 1) >= 0:  # North
        if maze[y_coord - 1][x_coord] == '-':
            paths.append(((x_coord, y_coord - 1)))
    if (y_coord + 1) < height:  # South
        if maze[y_coord + 1][x_coord] == '-':
            paths.append(((x_coord, y_coord + 1)))
    if (x_coord - 1) >= 0:  # West
        if maze[y_coord][x_coord - 1] == '-':
            paths.append(((x_coord - 1, y_coord)))
    if (x_coord + 1) < width:  # East
        if maze[y_coord][x_coord + 1] == '-':
            paths.append(((x_coord + 1, y_coord)))
    return paths


def get_start_finish(the_maze, as_node=False):
    start, finish = (), ()
    for pointer in range(len(the_maze[0])):
        if maze[0][pointer] == '-':
            start = (pointer, 0)
        if maze[-1][pointer] == '-':
            finish = (pointer, len(the_maze) - 1)
    if as_node:
        return Node(start[0], start[1]), Node(finish[0], finish[1])
    return start, finish


def get_maze(filename):
    total_maze = []
    with open(filename, 'r') as f:
        for line in f:
            total_maze.append(''.join(line.strip().split(' ')))

    total_maze_cleaned = []
    for row in total_maze:
        if '#' in row:
            total_maze_cleaned.append(row)
    return total_maze_cleaned


def get_paths(filename: str) -> {}:
    path_dict = {}
    with open(filename, 'r') as f:
        for line in f:
            line.strip()
        total_maze = f.readlines()

    total_maze_cleaned = []
    for line in total_maze:
        total_maze_cleaned.append(''.join(line.strip().split(' ')))

    # Change the next row searched based on;
    #   - The node is the (x, y) position of the cursor
    #   - the neighbour is the find_neighbour(previous_node)
    #   - The first neighbour that is a '-'
    #   - Taking into account the direction of the last node

    for line_index in range(len(total_maze_cleaned)):
        for character_index in range(len(total_maze_cleaned[line_index])):
            if total_maze_cleaned[line_index][character_index] == '-':
                new_node = Node(character_index, line_index)
                new_node_neighbours = [new_node, 0]
                path_dict.update({
                    new_node.get_position(): new_node_neighbours
                })
                prev_node = new_node.get_position()
    # Clean the path dictionary by removing invalid values
    # Go into each key.
    # Check if each value is part of the dictionary in the y++ and y-- rows

    updated_path_dict = {}
    keys = path_dict.keys()
    items = path_dict.items()

    for item in items:
        neighbours = list(item[1])
        for neighbour in item[1]:
            if neighbour not in keys:
                neighbours.remove(neighbour)
        updated_path_dict.update({
            item[0]: neighbours
        })
    # Assumes that the maze can be completed
    return updated_path_dict, list(keys)[0], list(keys)[-1], total_maze_cleaned


# Do find neighbours in dfs
# Make a clean function for the neighbours making sure they're not in the graph


def breadth_first_search(maze, start: (int, int), winner: (int, int)) -> (set, [], bool):
    stack = deque()
    stack.append((start, [start]))
    traversed = []
    is_visited = set()
    current_path = []
    while stack:
        current_node, current_path = stack.popleft()
        traversed.append(current_node)
        if current_node == (winner[0], winner[1]):
            is_visited.add(current_node)
            return is_visited, traversed, current_path, True
        if current_node not in is_visited:
            is_visited.add(current_node)
            for neighbour in get_neighbours(current_node, maze):
                stack.append((neighbour[0], current_path + [neighbour[0]]))

    return is_visited, traversed, current_path, False


def depth_first_search(maze, start: (int, int), winner: (int, int)) -> (set, [], bool):
    stack = deque()
    stack.append((start, [start]))
    traversed = []
    is_visited = set()
    current_path = []
    while stack:
        current_node, current_path = stack.pop()
        traversed.append(current_node)
        if current_node == (winner[0], winner[1]):
            is_visited.add(current_node)
            return is_visited, traversed, current_path, True
        if current_node not in is_visited:
            is_visited.add(current_node)
            for neighbour in get_neighbours(current_node, maze):
                stack.append((neighbour[0], current_path + [neighbour[0]]))

    return is_visited, traversed, current_path, False


def find_path(traversed):
    """
    :param traversed: The list of nodes that were visited in the search
    :return: the exit path of the maze
    """
    final_path = deque()  # Initialise the stack

    for node in traversed:  # Loop through the traversed nodes
        if node not in final_path:  # If the node is not already in the path
            final_path.append(node)
        else:  # If the node is found in the path again
            temp = ()
            while temp != node:
                temp = final_path.pop()  # Remove the redundant path
            final_path.append(temp)  # Add the diverging node back

    return final_path


def write_path(path_to_write, maze):
    matrix = []
    # print(" -> ".join(str(f) for f in path_to_write))
    for i in range(len(maze)):
        temp = []
        for j in range(len(maze[0])):
            temp.append(" ")
        matrix.append(temp)

    for x, y in path_to_write:
        matrix[y][x] = 'X'

    with open('solved_maze.txt', 'w') as f:
        for row in matrix:
            f.write(' '.join(str(a) for a in row) + '\n')


def visulizePath(mazes, visited, path):
    # Define colors for drawing
    WALL_COLOR = (0, 0, 0)
    FREE_COLOR = (255, 255, 255)
    VISITED_COLOR = (159, 43, 104)
    PATH_COLOR = (0, 255, 0)

    # Convert maze list to an image
    img_width, img_height = len(mazes[0]), len(mazes)
    img = Image.new('RGB', (img_width, img_height))
    draw = ImageDraw.Draw(img)
    for y in range(img_height):
        for x in range(img_width):
            if mazes[y][x] == '#':
                draw.rectangle([(x, y), (x + 1, y + 1)], fill=WALL_COLOR)
            else:
                draw.rectangle([(x, y), (x + 1, y + 1)], fill=FREE_COLOR)

    # Mark visited cells in the image
    for cell in visited:
        draw.rectangle([(cell[0], cell[1]), (cell[0] + 0.5, cell[1] + 0.5)], fill=VISITED_COLOR)

    # Mark path cells in the image
    for cell in path:
        draw.rectangle([(cell[0], cell[1]), (cell[0] + 0.5, cell[1] + 0.5)], fill=PATH_COLOR)

    # Save the image to a file
    img.save('maze_path.png')


def a_star_find_path(node_list: [Node]):
    path = []
    for node in reversed(node_list):
        path.append(node.parent)
    final_path = []
    for path_node in path:
        try:
            final_path.append(path_node.get_position())
        except AttributeError:
            continue
    return final_path


if __name__ == "__main__":
    print('--- MAZE LOADING ---')
    maze = get_maze('maze-Large.txt')
    start_node, goal_node = get_start_finish(maze, as_node=True)
    print("--- MAZE LOADED ---")
    startTime = time.time()
    a_star_path, completed = a_star_algorithm(maze, start_node, goal_node)

    # visited, traversed_nodes, paths, completed = depth_first_search(maze, start_node, winning_node)
    endTime = time.time()
    print(f"Is solved: {completed}")
    print(f"{endTime - startTime} seconds")
    # print(' -> '.join(str(node.get_position()) for node in a_star_path))

    paths = [node for node in a_star_path]
    path = a_star_find_path(paths)
    # print(" -> ".join(str(f) for f in list(visited)))
    write_path(path, maze)
    visulizePath(maze, path, path)

    print("Written to files")
