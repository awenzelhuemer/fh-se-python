# -*- coding: utf-8 -*-
"""
@author: Andreas Wenzelhuemer
"""

import random
import tracemalloc

directions = ('N', 'E', 'S', 'W')

def generate_walk(blocks: int = 1):
    """
    Generates walk with block count
    
    Parameters:
        block: Count for walk generation
        
    Returns:
        Iterable of random directions
    """
    if blocks < 0:
        raise ValueError("Blocks must be positive")
        
    for _ in range(blocks):
        yield random.choice(directions)

def decode_walk(walk):
    """
    Calculates end position of given walk
    
    Parameters:
        walk: List with directions
        
    Returns:
        Calculated final position after walk
    """
    x = 0
    y = 0
   
    for direction in walk:
        if direction == 'N':
            y += 1
        elif direction == 'S':
            y -= 1
        elif direction == 'E':
            x += 1
        elif direction == 'W':
            x -= 1
        else:
            raise ValueError("Walk contains an invalid direction")
    return (x, y)

def distance_manhattan(start, end):
    
    """
    Calculates manhattan distance from start and end point
    
    Parameters:
        start: Start point tuple with x and y coordinates
        end: End point tuple with x and y coordinates
        
    Returns:
        Manhattan distance as an integer value
    """
    
    return sum([abs(s - e) for s, e in zip(start, end)])
        
def do_walk(blocks, dist = distance_manhattan, gen_walk=True):
    """
    Generates walk and calculates distance
    
    Parameters:
        blocks: Count for walk generation
        dist: Distance calculation method, default is manhattan distance
        
    Returns:
        Tuple with generated walk and manhattan distance
    """
    walk = generate_walk(blocks)
    if gen_walk:
        walk = list(walk)
    start = (0,0)
    change = decode_walk(walk)
    end = (start[0] + change[0], start[1] + change[1])

    if gen_walk:
        return walk, dist(start, end)
    else:
        return None, dist(start, end)

def monte_carlo_walk_analysis(max_blocks, repetitions = 10000):
    """
    Generates walks from length 1 to block count with n repetitions
    
    Parameters:
        max_blocks: Max block count which should be generated
        repetitions: Count how often should each block count generation repeated
        
    Returns:
        Dictionary with max length as key and generated walks and distances as tuple
    """
    
    if max_blocks < 0:
        raise ValueError("Max blocks have to be greater zero")
    if repetitions < 0:
          raise ValueError("Repetitions have to be greater zero")
    
    walks = {}
    for blocks in range(1, max_blocks + 1):
        walks[blocks] = [do_walk(blocks) for _ in range(repetitions)]  
    return walks

def monte_carlo_walk(max_blocks, repetitions = 10000):
    """
    Generates walks from length 1 to block count with n repetitions
    
    Parameters:
        max_blocks: Max block count which should be generated
        repetitions: Count how often should each block count generation repeated
        
    Returns:
        Dictionary with max length as key and generated walks and distances as tuple
    """
    
    if max_blocks < 0:
        raise ValueError("Max blocks have to be greater zero")
    if repetitions < 0:
          raise ValueError("Repetitions have to be greater zero")
    
    walks = {}
    for blocks in range(1, max_blocks + 1):
        walks[blocks] = [do_walk(blocks, gen_walk=False) for _ in range(repetitions)]  
    return walks


if __name__ == "__main__":
    tracemalloc.start()
    monte_carlo_walk_analysis(20)
    current_size, peak_size = tracemalloc.get_traced_memory()
    print(f'Memory peak (monte_carlo_walk_analysis): {peak_size}')
    original = tracemalloc.take_snapshot()
    tracemalloc.reset_peak()

    monte_carlo_walk(20)
    current_size, peak_size = tracemalloc.get_traced_memory()
    print(f'Memory peak (monte_carlo_walk): {peak_size}')
    improved = tracemalloc.take_snapshot()
    
    print("Allocations:")
    for stat in improved.compare_to(original, 'traceback'):
        print(stat)

        
    
    