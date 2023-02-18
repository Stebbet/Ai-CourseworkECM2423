"""
author: Sam Tebbet
file: main.py
desctiption: depth first search on maxe-___.txt files to find exit
"""
import collections

"""
0 1 2
3 4 6 
6 7 8
"""


def find_neighbours(x, y):
    return [[x - 1, y - 1], [x, y - 1], [x + 1, y - 1],
            [x - 1, y], [], [x + 1, y],
            [x - 1, y + 1], [x, y + 1], [x + 1, y + 1]]


def load(file: str) -> (int, int, [[str]]):
    """
    Loads a file and returns the number of columns and rows
        :param file: the path of the file to be loaded
        :return (int, int, [str]): The number of rows, number of columns and the maze as a string
    """

    row_count = 0
    col_count = 0

    # Open and read the file
    with open(file, 'r') as f:
        lines = f.readlines()

    # Calculate the number of rows in the maze
    # Make the new string to return
    new_lines = []
    for line in lines:
        if '#' not in line or '-' not in line:
            break
        new_Line = ""
        for character in line:
            if character == "#" or character == "-":
                new_Line += character

        new_lines += new_Line
        row_count += 1

    # Calculate the number of columns in the maze

    col_count = len(new_lines[0])
    fin = 0
    for i in range(row_count):
        if lines[col_count - 1][i] == '-':
            fin = i
    f.close()

    return row_count, col_count, new_lines, fin

def get_graph(nodes, x_count, y_count):
    graph = {}
    for y in y_count:
        for x in x_count:
            graph[[nodes[y][x].x, nodes[y][x].y]] = nodes[y][x].find_neighbours()
    return graph


def get_path(x_count, y_count, maze_str: str) -> [[int]]:
    """
    Returns the path of valid nodes line in [[x, y]]
    :param x_count: number of columns
    :param y_count: number of rows
    :param maze_str: the maze as a string
    :return: array of path nodes in the maze
    """
    path = []
    for y in y_count:
        for x in x_count:
            if maze_str[y][x] == '-':
                path.append([x, y])
    return path


# Need to know if it is valid or not to then add to the list of nodes
def dfs(visited, graph, node, winner):
    if node == winner:
        return visited
    if node not in visited:
        visited.add(node)
        for neighbour in graph[node]:
            if neighbour[1]:
                dfs(visited, graph, neighbour[0], winner)


if __name__ == "__main__":
    maze = "maze-Easy.txt"
    rows, cols, maze_string, finish = load(maze)
    nodes = get_path(cols - 1, rows - 1, maze_string)
    visited = set()  # Keep track of visited nodes
    nodes_graph = get_graph(nodes)

    visited = dfs(visited, nodes_graph, [0, 1], [cols - 1][finish])
