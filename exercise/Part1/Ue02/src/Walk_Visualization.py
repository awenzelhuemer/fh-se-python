import turtle
import Basic_Library
import matplotlib.pyplot as plt

def get_degree(direction):
    """
    Returns degree depending on direction
    
    Parameters:
        direction: Current direction
        
    Returns:
        Rotation in degrees
    """
    if direction == 'N':
        return 270
    if direction == 'E':
        return 0
    elif direction == 'S':
        return 90
    elif direction == 'W':
        return 180
    else:
        raise ValueError("Invalid direction")

def generate_unique_colors(n):
    """
    Generates n unique colors

    Parameters:
        n: Number of unique colors

    Returns:
        List with unique colors
    """
    return plt.get_cmap(lut=n, name="tab20c")


def visualize_walk(t: turtle.Turtle, walk, start_pos: turtle.Vec2D, color):
    """
    Visualizes a given path

    Parameters:
        t: Turtle object
        walk: List with given directions
        start_pos: The position where the drawing should start
    """
    # Set start position
    t.penup()
    t.goto(start_pos)
    t.pendown()
    # Set color and start point
    t.color(color[:-1])
    t.dot()
    # Set initial degree value
    previous_degree = 0
    for direction in walk:
        degree = get_degree(direction)
        t.right(-previous_degree + degree)
        previous_degree = degree
        t.forward(60)
    # Set end point
    t.dot()

def visualize_walks(t: turtle.Turtle, walks):
    """
    Visualizes given paths

    Parameters:
        walks: List with walks
    """
    t.speed(500)
    (x, y) = t.pos()
    colors = generate_unique_colors(len(walks))
    index = 0

    for walk in walks:
        visualize_walk(t, walk, (x, y), colors(index))
        index += 1
        # Add offset
        x += 2
        y += 2

blocks = 15
walks = [list(Basic_Library.generate_walk(blocks)) for _ in range(10)]
visualize_walks(turtle.Turtle(), walks)

turtle.mainloop()