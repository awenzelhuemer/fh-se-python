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
   
    for direction in walk:
        if(direction == 'N'):
            dy += 1
        elif(direction == 'S'):
            dy -= 1
        elif(direction == 'E'):
            dx += 1
        elif(direction == 'W'):
            dx -= 1
        else:
            raise KeyError("Invalid direction")
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

def monte_carlo_walk_analysis(max_blocks, repetitions = 10000):
    
    """
    Generates walks from length 1 to block count with n repetitions
    
    Parameters:
        max_blocks: Max block count which should be generated
        repetitions: Count how often should each block count generation repeated
        
    Returns:
        Dictionary with max length as key and generated walks and tuples as tuple
    """
    
    if(max_blocks < 1):
        raise ValueError("Max blocks have to be greater zero")
    if(repetitions < 1):
          raise ValueError("Repetition has to be greater zero")
    
    walks = {}
    for blocks in range(max_blocks):
        current_walks = [do_walk(blocks + 1) for _ in range(repetitions)]
        walks[max(walk[1] for walk in current_walks)] = current_walks  
    return walks


def test_generate_walk():
    
    print('-- test_generate_walk --')
    
    print('- With default parameter')
    print(list(generate_walk()))
    
    for value in [-1, 1, 10]:
        print(f'- With value={value}')
        try:
            print(list(generate_walk(value)))
        except ValueError as error:
            print(f'Exception thrown: {error}')

def test_decode_walk():
    
    print('-- test_decode_walk --')
    
    print('- Empty list')
    print(decode_walk([]))
    
    print('With list ["N", "N", "E", "E"]')
    print(decode_walk(['N', 'N', 'E', 'E']))
    
    try:
        print('- With invalid value')
        print(decode_walk(['N','O']))
    except KeyError as error:
         print(f'Exception thrown: {error}')
         
def test_distance_manhattan():
    
    print('-- test_distance_manhattan --')
    
    print('- With same start and end points')
    print(distance_manhattan((0, 0), (0, 0)))
    
    print('- With start point(0, 0) end point(2, 3)')
    print(distance_manhattan((0, 0), (2, 3)))
    
def test_do_walk():
    print('-- test_do_walk --')
    
    print('- With valid parameters')
    print(do_walk(10))
    
    print('- With fake distance function')
    print(do_walk(5, lambda start, end: 0))

def test_monte_carlo_walk_analysis():
    print('-- test_monte_carlo_walk_analysis --')
    
    print('- With valid parameters')
    print(monte_carlo_walk_analysis(5, 5))
    
    try:
        print('- Test with invalid parameter for max_blocks')
        print(monte_carlo_walk_analysis(-1))
    except Exception as error:
        print(f'Exception thrown: {error}')
        
    try:
        print('- Test with invalid parameter for repetition')
        print(monte_carlo_walk_analysis(10, -1))
    except Exception as error:
        print(f'Exception thrown: {error}')

test_generate_walk()
test_decode_walk()
test_distance_manhattan()
test_do_walk()
test_monte_carlo_walk_analysis()

# print(distance_manhattan((0,0), endPoint))
# print(monte_carlo_walk_analysis(2, 10))


        
    
    