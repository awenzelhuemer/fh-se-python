from typing import Dict
import Basic_Library

def roundtrips_with_length_4(walks: Dict):
    print("-- roundtrips_with_length_4 --")
    block_size = 4
    if(block_size in walks.keys()):
        roundtrips = [walk[0] for walk in walks[block_size] if walk[1] == 0]
        print(len(roundtrips))
    else:
        print("No trips found")

walks = Basic_Library.monte_carlo_walk_analysis(50)
roundtrips_with_length_4(walks)