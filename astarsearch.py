"""
A* Algorithm implementation for ECM2423 Artificial Intelligence and Applications
@author Sam Tebbet
"""

import time
import math
from visualizer import visualize_path
from bfs_dfs import generate_statistics, get_maze, get_start_finish, get_neighbours
import heapq


def get_manhattan(current_node: (int, int), end_node: (int, int)) -> int:
    """
    The function gets the manhattan distance between two node coordinates
    :param current_node: The current node
    :param end_node: The goal node
    :return: The manhattan distance between the two coordinates
    """
    dx = abs(end_node[0] - current_node[0])
    dy = abs(end_node[1] - current_node[1])
    return dx + dy


def get_euclidian(current_node: (int, int), end_node: (int, int)) -> float:
    """
    The function finds the euclidian distance between two node coordinates
    :param current_node: The current node
    :param end_node: The goal node
    :return: Euclidean distance between the two coordinates
    """
    dx = current_node[0] - end_node[0]
    dy = current_node[1] - end_node[1]
    return math.sqrt(dx * dx + dy * dy)


def final_path(node: (int, int), traversed_dict: {}) -> ([int, int], [(int, int)]):
    """
    This function finds the final path from the dictionary of traversed by backtracking
    :param node: The end node to start backtracking from
    :param traversed_dict: Dictionary of all the traversed nodes
    :return path, []: The final path and a list of the traversed nodes
    """
    path = [node]
    while node in traversed_dict:
        node = traversed_dict[node]
        path.append(node)
    path.reverse()
    return path, traversed_dict.keys()


def a_star_search(maze: [[str]], start: (int, int), goal: (int, int)) -> ({}, bool):
    """
    This function runs the A* search algorithm on an inputted maze to find a route out
    :param maze: The maze represented as a 2D list
    :param start: The start of the maze as coordinates (int, int)
    :param goal: The end of the maze as coordinates (int, int)
    :return paths, counter, bool:
        paths: Dictionary of the nodes reached
        counter: The number of nodes visited
        bool: if the maze was solved or not
    """

    counter = 0
    paths = {}
    queue = []
    heapq.heappush(queue, (0, start))
    g_dict = {start: 0}
    f_dict = {start: get_manhattan(start, goal)}

    while len(queue) != 0:  # While the priority queue is not empty
        counter += 1
        node = heapq.heappop(queue)
        priority, current_node = node
        x, y = current_node

        # If the goal is reached
        if (x, y) == (goal[0], goal[1]):
            # The search succeeded, return True for completed
            return paths, counter, True

        # Iterate through the valid neighbours / successors
        for successor in get_neighbours(current_node, maze):
            next_g = g_dict[current_node] + 1  # The distance from one node to the next is always 1
            if successor not in g_dict or next_g < g_dict[successor]:

                # Update the dictionaries with the successor data
                paths[successor] = current_node
                g_dict[successor] = next_g
                f_dict[successor] = g_dict[successor] + get_manhattan(successor, goal)

                # Push the successor to the Priority Queue
                heapq.heappush(queue, (f_dict[successor], successor))

    # The search failed, return False for completed
    return paths, counter, False


def run_a_star(filename):
    """
    :param filename: The name of the maze file
    """
    maze = get_maze(filename)  # Get the 2D list representation of the maze
    start_node, goal_node = get_start_finish(maze)

    start_time = time.time()
    a_star_path, count, completed = a_star_search(maze, start_node, goal_node)
    end_time = time.time()

    difference = end_time - start_time
    path, visited = final_path(goal_node, a_star_path)

    visualize_path(maze, visited, path)
    generate_statistics(time_diff=difference, num_steps=count, completed=completed)
