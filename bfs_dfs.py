"""
Depth-first and Breadth-first search implementations for ECM2423 Artificial Intelligence and Applications
@author Sam Tebbet
"""

from collections import deque
import time
from visualizer import visualize_path


def bfs(maze: [[str]], start: (int, int), winner: (int, int)) -> (set, [], bool):
    """
    This function runs the breadth-first search algorithm on an inputted maze to find a route out
    :param maze: The maze represented as a 2D list
    :param start: The start of the maze as coordinates (int, int)
    :param winner: The end of the maze as coordinates (int, int)
    :return traversed, current_path, bool:
        traversed: List of all the traversed nodes
        current_path: List of all the nodes in the final path
        counter: The number of nodes visited
        bool: True if the maze is solved, False if not
    """
    counter = 0
    queue = deque()
    queue.append((start, [start]))
    traversed = []
    is_visited = set()
    current_path = []

    while queue:  # While the stack is not empty
        counter += 1
        current_node, current_path = queue.popleft()  # Pop left to represent a queue
        traversed.append(current_node)

        # If the node is the winning node
        if current_node == (winner[0], winner[1]):
            is_visited.add(current_node)
            return traversed, current_path, counter, True

        # If the node has already been visited
        if current_node not in is_visited:
            is_visited.add(current_node)

            # Append all the valid neighbours to the queue
            for neighbour in get_neighbours(current_node, maze):
                queue.append((neighbour, current_path + [neighbour]))
    return traversed, current_path, counter, False


def dfs(maze, start: (int, int), winner: (int, int)) -> (set, [], bool):
    """
    This function runs the depth-first search algorithm on an inputted maze to find a route out
    :param maze: The maze represented as a 2D list
    :param start: The start of the maze as coordinates (int, int)
    :param winner: The end of the maze as coordinates (int, int)
    :return traversed, current_path, bool:
        traversed: List of all the traversed nodes
        current_path: List of all the nodes in the final path
        counter: The number of nodes visited
        bool: True if the maze is solved, False if not
    """
    counter = 0
    stack = deque()
    stack.append((start, [start]))
    traversed = []
    is_visited = set()
    current_path = []

    while stack:
        counter += 1
        current_node, current_path = stack.pop()  # Pop right to represent a stack
        traversed.append(current_node)

        # If the node is the winning node
        if current_node == (winner[0], winner[1]):
            is_visited.add(current_node)
            return traversed, current_path, counter, True

        # If the node has not been visited already
        if current_node not in is_visited:
            is_visited.add(current_node)

            # Add the valid neigbours to the stack
            for neighbour in get_neighbours(current_node, maze):
                stack.append((neighbour, current_path + [neighbour]))

    return traversed, current_path, counter, False


def get_neighbours(node: (int, int), maze: [[str]]) -> [(int, int)]:
    """
    This function find the valid ('-'), neighbours to a node and returns them
    :param node: The coordinates of the node
    :param maze: The maze represented as a 2D list
    :return paths: A list of all the valid neighbours
    """
    x = node[0]
    y = node[1]
    width = len(maze[0])
    height = len(maze)
    paths = []

    if (y - 1) >= 0:  # North
        if maze[y - 1][x] == '-':
            paths.append((x, y - 1))

    if (y + 1) < height:  # South
        if maze[y + 1][x] == '-':
            paths.append((x, y + 1))

    if (x - 1) >= 0:  # West
        if maze[y][x - 1] == '-':
            paths.append((x - 1, y))

    if (x + 1) < width:  # East
        if maze[y][x + 1] == '-':
            paths.append((x + 1, y))

    return paths


def get_maze(filename):
    """
    This reads a maze from a file and returns the maze represented as a 2D list
    :param filename: The maze file
    :return: The maze represented as a 2D list
    """
    total_maze = []
    with open(filename, 'r') as f:
        for line in f:
            total_maze.append(''.join(line.strip().split(' ')))

    total_maze_cleaned = []
    for row in total_maze:
        if '#' in row:
            total_maze_cleaned.append(row)
    return total_maze_cleaned


def get_start_finish(maze: [[str]]) -> ((int, int), (int, int)):
    """
    This function gets the position of the start node and the goal node
    :param maze: The maze represented as a 2D list
    :return start, finish: The coordinates of the start node and the goal node
    """
    start, finish = (), ()
    for pointer in range(len(maze[0])):
        if maze[0][pointer] == '-':
            start = (pointer, 0)
        if maze[-1][pointer] == '-':
            finish = (pointer, len(maze) - 1)
    return start, finish


def generate_statistics(time_diff=0.0, num_steps=0, final_path=deque(), traversed_nodes=[], completed=False,
                        verbosity=0):
    """
    :param time_diff: The time it took for the algorithm to complete
    :param num_steps: The number of steps that the algorith took
    :param final_path: The path to solve the maze
    :param traversed_nodes: A list of all the nodes that were traversed
    :param completed: If the maze was solved or not
    :param verbosity: How verbose the user wants the statistics. default = 0
    """
    print(f'Maze solved: {completed}')
    print(f'Time taken: {time_diff}')
    print(f'Steps taken: {num_steps}')
    if verbosity == 1:  # Level 1 verbosity prints the final path
        print(f'Path to goal: {final_path}')
    elif verbosity == 2:  # Level 2 verbosity prints the final path and traversed nodes
        print(f'Path to goal: {final_path}')
        print(f'Traversed Nodes: {traversed_nodes}')


def run_dfs_bfs(filename, solver):
    """
    This function runs either the breadth-first or depth first algorithm on a specified maze
    :param filename: The name of the maze file
    :param solver: The maze algorithm to be run
    """

    maze = get_maze(filename)
    start_node, goal_node = get_start_finish(maze)

    if solver == 0:  # For depth first search user enters 0
        start_time = time.time()
        traversed_nodes, paths, count, completed = dfs(maze, start_node, goal_node)
        end_time = time.time()
    else:  # Otherwise it is breadth first
        start_time = time.time()
        traversed_nodes, paths, count, completed = bfs(maze, start_node, goal_node)
        end_time = time.time()

    difference = end_time - start_time
    generate_statistics(difference, count, paths, traversed_nodes, completed)
    visualize_path(maze, traversed_nodes, paths)
