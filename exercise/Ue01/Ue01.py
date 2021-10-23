# -*- coding: utf-8 -*-
"""
@author: Andreas Wenzelhuemer
"""

import random

directions = ('N', 'E', 'S', 'W')

def generate_walk(block = 1):
    """
    Generates walk with block count
    
    Parameters:
        block: Count for walk generation
        
    Returns:
        Iterable of random directions
    """
    if(block < 1):
        raise ValueError("Block has to be greater zero")
        
    for _ in range(block):
        yield random.choice(directions)

def decode_walk(walk):
    """
    Calculates end position of given walk
    
    Parameters:
        walk: List with directions
        
    Returns:
        Calculated final position after walk
    """
    dx = 0
    dy = 0
   
    for step in walk:
        if(step == 'N'):
            dy += 1
        elif(step == 'S'):
            dy -= 1
        elif(step == 'E'):
            dx += 1
        else:
            dx -= 1
    return dx, dy


def distance_manhattan(start, end):
    
    """
    Calculates manhattan distance from start and end point
    
    Parameters:
        start: Start point tuple with x and y coordinates
        end: End point tuple with x and y coordinates
        
    Returns:
        Manhattan distance as an integer value
    """
    
    return abs(start[0] - end[0]) + abs(start[1] - end[1])
        

def do_walk(blocks, dist = distance_manhattan):
    """
    Generates walk and calculates distance
    
    Parameters:
        blocks: Count for walk generation
        dist: Distance calculation method, default is manhattan distance
        
    Returns:
        Tuple with generated walk and manhattan distance
    """
    
    walk = list(generate_walk(blocks))
    distance = dist((0, 0), decode_walk(walk))
    return (walk, distance)

def monte_carlo_walk_analysis(max_blocks, repitions = 10000):
    
    """
    Generates walks from length 1 to block count with n repitions
    
    Parameters:
        max_blocks: Max block count which should be generated
        repitions: Count how often should each block count generation repeated
        
    Returns:
        Dictionary with max length as key and generated walks and tuples as tuple
    """
    
    if(max_blocks < 1):
        raise ValueError("Max blocks have to be greater zero")
    if(repitions < 1):
          raise ValueError("Repition has to be greater zero")
    
    walks = {}
    for blocks in range(1, max_blocks + 1):
        current_walks = [do_walk(blocks) for _ in range(repitions)]
        walks[max(x[1] for x in current_walks)] = current_walks  
    return walks

walks = generate_walk(10)
endPoint = decode_walk(walks)

print(distance_manhattan((0,0), endPoint))
print(monte_carlo_walk_analysis(2, 10))


        
    
    