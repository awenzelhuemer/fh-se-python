from pprint import pprint
from typing import Dict
import statistics
import Basic_Library

# Question 1
# How many roundtrips of length 4 (including duplicates) have been generated?
# Roundtrips are tours of a distance of zero from the starting position and the
# length of a roundtrip is the number of walked blocks.
def roundtrips_with_length_4(walks: Dict):
    ''' Calculates roundtrips with length of 4 '''
    print("-- Roundtrips with length 4 --")
    roundtrips = [walk for walk, distance in walks[4] if distance == 0]
    print(len(roundtrips))

# Question 2
# Which different (unique) roundtrips have been identified for the different
# maximum lengths? List the number of identified unique roundtrips for each
# maximum length and the first 10 roundtrips per maximum length (the others
# can be omitted).
def unique_roundtrips(walks: Dict):
    ''' Calculates all unique round trips '''
    all_roundtrips = {length: [walk for walk, distance in walks[length] if distance == 0] for length in walks}

    print("-- First 10 roundtrips --")
    first_ten_roundtrips = {length: all_roundtrips[length][:10] for length in all_roundtrips}
    print(len(first_ten_roundtrips))

    print("-- Unique roundtrips --")
    flatted_roundtrips = [walk for key in all_roundtrips # Iterate over all round trips
                                for walk in all_roundtrips[key]] # Get walk from each dictionary entry
    unique_roundtrip_set = set(tuple(trip) for trip in flatted_roundtrips) # By creating a set all duplicates get deleted
    all_unique_roundtrips = [list(trip) for trip in unique_roundtrip_set] # Convert tuples to list
    print(len(all_unique_roundtrips))

# Question 3
# What is the average and median1 distance for walks of maximum lengths 5, 10,
# 15, 20, 25?
def average_median(walks: Dict):
    ''' Calculates average and median for walks of length 5, 10, 15, 20 and 25.'''
    print("-- Average and median --")
    for length in [5, 10, 15, 20, 25]:
        distances = [distance for _, distance in walks[length]]
        print(f'Average for {length}: {statistics.mean(distances)}')
        print(f'Median for {length}: {statistics.median(distances)}')

# Question 4
# What is the percentage of walks that end at a position with a maximum possible
# distance from the starting distance per maximum walk length?
def percentage_max_walk_distance(walks: Dict):
    ''' Calculates the percentage of walks that end at a position with a maximum distance.'''
    print("-- Percentage of max walks --")
    walk_count = len([walk for key in walks for walk, _ in walks[key]])
    max_distance_count = len([walk for key in walks
                                        for walk, distance in walks[key] if distance == key])
    print(f"{round((max_distance_count / walk_count) * 100, 2)}%")                                                

# Question 5
# Which distinct straight walks have been generated; walks that continue in the
# same direction? Therefore, you have to implement a predicate function
# def checkEqual(iterator) that checks whether an iterator consists only of
# one different element. Try to avoid additional memory allocation within the
# checkEqual function.
def check_equal(iterator):
    ''' Checks if each element in list has the same value'''
    if len(iterator) == 0:
        return True
    for element in iterator:
        if element != iterator[0]:
            return False
    return True

def straight_walks(walks: Dict):
    ''' Checks walks for straight walks'''
    print("-- Check straight walks --")
    # Check for each walk if it only contains one different element with the check_equal function
    straight_walks = [walk for key in walks
                            for walk, _ in walks[key] if check_equal(walk)]
    straight_unique_walks_set = set(tuple(walk) for walk in straight_walks) # Remove duplicates by creating a set
    straight_unique_walks = [list(walk) for walk in straight_unique_walks_set] # Change set to list
    pprint(straight_unique_walks)

def main():
    walks = Basic_Library.monte_carlo_walk_analysis(50)
    roundtrips_with_length_4(walks)
    unique_roundtrips(walks)
    average_median(walks)
    percentage_max_walk_distance(walks)
    straight_walks(walks)

if __name__ == "__main__":
    main()