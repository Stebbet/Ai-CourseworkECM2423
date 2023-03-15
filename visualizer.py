"""
Script to visualise the maze as a png for ECM2423 Artificial Intelligence and Applications
@author Sam Tebbet
"""

# Import Pillow as the image library
from PIL import Image, ImageDraw


def visualize_path(maze: [[str]], traversed: [(int, int)], path: [(int, int)]):
    """
    This function makes an png of the maze with the traversed nodes highlighted and the path shows as well
    :param maze: The maze represented as a 2D list
    :param traversed: A list of all the traversed nodes
    :param path: A list of the path nodes
    """

    # Define colors for drawing
    wall_colour = (0, 0, 0)
    nothing_colour = (255, 255, 255)
    traversed_colour = (178, 102, 255)
    path_colour = (0, 255, 0)

    # Make the image at the width and height of the maze
    img_width, img_height = len(maze[0]), len(maze)
    img = Image.new('RGB', (img_width, img_height))
    draw = ImageDraw.Draw(img)

    # Draw the maze walls and gaps
    for y in range(img_height):
        for x in range(img_width):
            if maze[y][x] == '#':
                draw.rectangle((x, y, x + 1, y + 1), fill=wall_colour)
            else:
                draw.rectangle((x, y, x + 1, y + 1), fill=nothing_colour)

    # Show the visited cells in the image
    for cell in traversed:
        draw.rectangle((cell[0], cell[1], cell[0] + 0.5, cell[1] + 0.5), fill=traversed_colour)

    # Show the path cells in the image
    for cell in path:
        draw.rectangle((cell[0], cell[1], cell[0] + 0.5, cell[1] + 0.5), fill=path_colour)

    # Save the image to a file
    img.save('maze_path.png')
