"""
Scan the file
Find the path nodes on that file and add them to an 2D array like [[ Node(x, y) ]]
Find the start node
Find the finish node
"""

class Node:
    def __init__(self, x, y):
        visited = False
        self.x = x
        self.y = y
        self.visited = False
        path = True

    def find_neighbours(self):
        neighbours = []
        neighbours.append((self.x - 1, self.y))  # West
        neighbours.append((self.x, self.y + 1))  # South
        neighbours.append((self.x + 1, self.y))  # East
        if self.y - 1 >= 0:
            neighbours.append((self.x, self.y - 1))  # North

        return neighbours

    def get_position(self):
        return self.x, self.y


def get_paths(filename: str) -> {}:
    path_dict = {}

    with open(filename, 'r') as f:
        total_maze = f.readlines()

    total_maze_cleaned = []
    for line in total_maze:
        total_maze_cleaned.append(''.join(line.strip().split(' ')))

    for line_index in range(len(total_maze_cleaned)):
        for character_index in range(len(total_maze_cleaned[line_index])):
            if total_maze_cleaned[line_index][character_index] == '-':
                new_node = Node(character_index, line_index)
                new_node_neighbours = new_node.find_neighbours()
                path_dict.update({
                    new_node.get_position(): new_node_neighbours
                })

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

    return updated_path_dict, list(keys)[-1], list(keys)[0]




def depth_first_search(filename):
    def dfs(graph, node):
        if node is winner:
            visited.append(node)
            return
        else:
            if node not in visited:
                visited.append(node)
                for neighbour in graph[node]:
                    dfs(graph, neighbour)

    nodes, winner, start = get_paths(filename)
    visited = []
    dfs(nodes, start)
    traverse_path = []
    for i in visited:
        if i == winner:
            traverse_path.append(i)
            break
        traverse_path.append(i)

    return traverse_path, visited


trav, vis = depth_first_search('maze-Easy.txt')
print(f"{len(trav)} : {len(vis)}")

