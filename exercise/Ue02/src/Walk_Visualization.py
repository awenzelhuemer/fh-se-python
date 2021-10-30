import turtle
import Basic_Library
import random


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

def get_random_color():
    """
    Generates random number

    Returns:
        Random color as string
    """
    return "#" + ''.join([random.choice('0123456789ABCDEF') for i in range(6)])


def visualize_walk(t: turtle.Turtle, walk, start_pos: turtle.Vec2D):
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
    t.color(get_random_color())
    t.dot()
    # Set initial degree value (default is rotated to the right)
    previous_degree = 0
    for direction in walk:
        degree = get_degree(direction)
        t.right(-previous_degree + degree)
        previous_degree = degree
        t.forward(60)
    # Set end point
    t.dot()

t = turtle.Turtle()
t.speed(500)
(x, y) = t.pos()
walks = Basic_Library.monte_carlo_walk_analysis(10, repetitions=5)
for key in walks:
    for walk in walks[key]:
        visualize_walk(t, walk[0], (x, y))
        # Add offset each time
        x += 2
        y += 2

turtle.mainloop()