"""
Coursework for ECM2423 Artificial Intelligence and Applications
author: Sam Tebbet
description: main file
"""
# Import the algorithms
from astarsearch import run_a_star
from bfs_dfs import run_dfs_bfs


def write_path(path_to_write: [(int, int)], maze: [[str]]):
    """
    This function writes the final path to a file for the user to see
    :param path_to_write: The final path represented as a list of coordinates
    :param maze: The maze
    """
    matrix = []  # Array for the final path to be displayed in

    # Filling the matrix with spaces to make it the size of the maze and for formatting
    for i in range(len(maze)):
        temp = []
        for j in range(len(maze[0])):
            temp.append(" ")
        matrix.append(temp)

    # Adding the path nodes
    for x, y in path_to_write:
        matrix[y][x] = 'X'

    # Write matrix to a file
    with open('solved_maze.txt', 'w') as f:
        for row in matrix:
            f.write(' '.join(str(a) for a in row) + '\n')


def ask_for_file() -> str:
    """
    Asking the user which maze they want to run
    :return: The filename of the maze they want
    """
    user_input = int(
        input(f"What maze do you want to run?\n  - Easy = 0\n  - Medium = 1\n  - Large = 2\n  - VLarge = 3\n"))
    while True:
        if user_input == 0:
            return 'maze-Easy.txt'
        elif user_input == 1:
            return 'maze-Medium.txt'
        elif user_input == 2:
            return 'maze-Large.txt'
        elif user_input == 3:
            return 'maze-VLarge.txt'

        user_input = int(
            input(f"Number not valid. Try Again:\n  - Easy = 0\n  - Medium = 1\n  - Large = 3\n  - VLarge = 4\n"))


def ask_for_search() -> (str, int):
    """
    Asking the user which search algorithm they want to run, and calling ask_for_file as well
    :return: The filename of the maze they want and an integer representation of the search algorithm the user wants
    """
    user_input = int(
        input(f"What algorithm do you want to run?:\n  - Depth-first = 0\n  - Breadth First = 1\n  - A* Search = 2\n")
    )
    while True:
        if user_input == 0 or user_input == 1 or user_input == 2:
            file = ask_for_file()
            return file, user_input
        user_input = int(
            input(f"Number not valid. Try Again:\n  - Depth-first = 0\n  - Breadth First = 1\n  - A* Search = 2\n"))


if __name__ == "__main__":
    file, search = ask_for_search()
    if search == 2:
        run_a_star(file)
    else:
        run_dfs_bfs(file, search)

    print("Finished")
